import json
import websocket
import requests
from random import * 
from time import sleep
from bs4 import BeautifulSoup as BS

class Bot:

    calling_msg = '~점심'
    def __init__(self, slacker, config ):
        #print('init')
        self.slacker = slacker
        self.config = config 
        #print(self.config)

    def loop(self):

        #print('start loop')

        count = 0
        list= []
        while True:
            sleep(2)
            channel, msg = self._read()
            if not channel or not  msg:
                continue
            if count==0  :
                list = self._crwaling(msg)

                #print(list)
            count =randint(0,59)
            msg = '우리 이거먹어요!\n'+list[count]
            #print('befor send')

            self._send(channel,msg)
    
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
                ##print(event)
                #print(event) 
                channel, msg = self._parse(event)
                if not channel or not  msg:
                    continue

                break
            except websocket.WebSocketTimeoutException:
                self._socket.send(json.dumps({'type':'ping'}))
            
            except websocket.WebSocketConnectionClosedException:
                #print("Connection closed")
                break

            except Exception as e :
                #print(e)
                break

        ws.close()
       
        return channel, msg

    def _send(self,channel,msg):
        self.slacker.chat.post_message(channel, msg, as_user=True)

    def _parse(self, event):
        if event['type'] != 'message' or event['text'] != '~점심':
            return None,None

        channel = event['channel']
        #print(channel) 
        text = event['text'].replace(self.calling_msg, '').strip()
        #전체
        if text == '':
            text = 'all'
        #한식, 양식, 중식, 일식 그대로

        msg = text
        #print(msg)
        return channel, msg 

    def _crwaling(self,msg):
        #language: kor
        #device_uuid: bcp9t15471855646162322dtfhz
        #device_type: web
        #start_index: 0
        #request_count: 20
        #keyword: 필동
        #filter: {"subcuisine_codes":[],"metro_codes":[],"price_codes":["2","1"],"cuisine_codes":[2],"is_parking_available":0} 
            
        # 한식 1 일식 2 중식 3 양식  4
        cuisine_arr = []
        if msg == 'all':
           cuisine_arr.append(1) 
           cuisine_arr.append(2) 
           cuisine_arr.append(3) 
           cuisine_arr.append(4) 
        if msg == '한식':
            cuisine_arr.append(1)
        if msg == '일식':
            cuisine_arr.append(2)
        if msg == '중식':
            cuisine_arr.append(3)
        if msg == '양식':
            cuisine_arr.append(4)
        # 가격 제한 코드 : 만원미만 1, 만원대 2
        start_index = 0,20,40,60
        tlist = []
        for index in start_index:
            filter = {"subcuisine_codes":[],"metro_codes":[],"price_codes":["1"],"cuisine_codes":cuisine_arr,"is_parking_available":0} 
            params = { 'language':'kor', 'device_uuid': 'bcp9t15471855646162322dtfhz', 'device_type':'web','start_index':index,'request_count':20,'keyword':'충무로역','filter':json.dumps(filter), 'order_by':2}
            #print(params)
            url = self.config["DEFAULT"]['URL']
            headers = {'User-agent': 'your bot 0.1'}
            get_data = requests.post(url,headers=headers, data= params )
            json_list = json.loads(get_data.text)
            for restaurant in json_list['result']:
                rlist = []
                name = '```\n식당이름 : ' + restaurant['restaurant']['name']
                address = '주소 : ' +  restaurant['restaurant']['address']
                rating = '점수 : ' +  str(restaurant['restaurant']['rating'])
                web_url = restaurant['restaurant']['web_url']
                menu_list = self._getPrice(web_url)
                str_menu = '\n-----------'.join(menu_list)
                rlist.append(name)
                rlist.append(address)
                rlist.append(rating)
                rlist.append('```\n'+web_url)
                if len(menu_list) >0 :
                    rlist.append(str_menu)
                string = '\n'.join(rlist)
                tlist.append(string) 
        return tlist 

    def _getPrice(self, link):
        get_data = requests.get(link)
        #print(link)
        soup = BS(get_data.text,'html.parser')
        menu_list = soup.select('.Restaurant_MenuItem')
        return menu_list
