import json
import websocket

class Bot:
   
    calling_msg = '~점심'
    def __init__(self, slacker, config ):
        print('init')
        self.slacker = slacker
        self.config = config 

    def loop(self):
        print('start loop')

        while True:
           channel, msg = self._read()
           print('befor send')
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
                #print(event)
                print(event) 
                channel, msg = self._parse(event)
                if not channel or not  msg:
                    continue
                break
                print('here')
            except websocket.WebSocketTimeoutException:
                self.ws.send(json.dumbs({'type':'ping'}))

            except Exception as e :
                print(e)
                break

        ws.close()
       
        return channel, msg

    def _send(self,channel,msg):
        msg = msg + '를 선택하셨습니다'
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


