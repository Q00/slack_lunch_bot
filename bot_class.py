import json
import websocket
import requests

class Bot:
   
    calling_msg = '~점심'
    def __init__(self, slacker, config ):
        print('init')
        self.slacker = slacker
        self.config = config 
        print(self.config)

    def loop(self):
        print('start loop')
        count =0
        list= []
        while True:
           channel, msg = self._read()
           if count==0  :
               list = self._crwaling(msg)
           else:
               pass
           msg = '대표님 점심으로 이건 어때요?\n'+list[count]
           print('befor send')
           self._send(channel,msg)
           count+=1 
    
    def _read(self):
        slacker = self.slacker
        res  = slacker.rtm.connect()
        endpoint = res.body['url']

        ws =websocket.create_connection(endpoint)
        ws.settimeout(60)
        self._socket = ws
        while True:
            try:
                event = json.loads(self._socket.recv())
                #{'type': 'message', 'user': 'UEHAZ63AP', 'text': '~점심', 'client_msg_id': '5cce9b39-9d70-4584-9776-9d91c1ab034c', 'team': 'TEH919RMJ', 'channel': 'CEHAZ69A7', 'event_ts': '1547104675.002500', 'ts': '1547104675.002500'}
                #print(event)
                print(event) 
                channel, msg = self._parse(event)
                if not channel or not  msg:
                    continue

                break
            except websocket.WebSocketTimeoutException:
                self._socket.send(json.dumbs({'type':'ping'}))

            except Exception as e :
                print(e)
                break

        ws.close()
       
        return channel, msg

    def _send(self,channel,msg):
        self.slacker.chat.post_message(channel, msg, as_user=True)

    def _parse(self, event):
        if event['type'] != 'message' or event['text'] != '~점심':
            return None,None

        channel = event['channel']
        print(channel) 
        text = event['text'].replace(self.calling_msg, '').strip()
        #전체
        if text == '':
            text = 'all'
        #한식, 양식, 중식, 일식 그대로

        msg = text
        print(msg)
        return channel, msg 

    def _crwaling(self,msg):
        api_key = self.config['DEFAULT']['API_KEY']
        query = '필동 식당'
        #https://maps.googleapis.com/maps/api/place/
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        #https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&type=restaurant&keyword=cruise&key=YOUR_API_KEY
 
        params= {'key':api_key,'location':'37.561306,126.994500','rankby':'distance','keyword':'필동 식당','type':'restaurant'}
        
        get_data = requests.get(url,params=params)
        print(get_data.text) 

        data_list = json.loads(get_data.text)
        next_page_token = data_list['next_page_token']
         
        list = []
        for data in data_list['results']:
            vicinity = data['vicinity']
            user_ratings_total = data['user_ratings_total']
            rating = data['rating']
            name = data['name']
            restraunt = f'''
            ```
            이름 : {name}
            주소 : {vicinity}
            평점 : {rating}
            유저평가수 : {user_ratings_total}
            ```'''
            list.append(restraunt)
        
        return list 
