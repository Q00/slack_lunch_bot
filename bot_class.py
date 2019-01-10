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

        while True:
           channel, msg = self._read()
           msg = self._crwaling(msg)
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
        api_key = self.config['DEFAULT']['API_ID']
        api_secret = self.config['DEFAULT']['API_SECRET']
        
        #curl "https://naveropenapi.apigw.ntruss.com/map-place/v1/search?query={장소_명칭}&coordinate={검색_중심_좌표}" \	-H "X-NCP-APIGW-API-KEY-ID: {애플리케이션 등록 시 발급받은 client id값}" \	-H "X-NCP-APIGW-API-KEY: {애플리케이션 등록 시 발급받은 client secret값}" -v

        query = '식당'
        coordinate = '126.9968285,37.5620175'
        url = f'https://naveropenapi.apigw.ntruss.com/map-place/v1/search?query={query}&coordinate={coordinate}&count=100'
        headers = {
                'X-NCP-APIGW-API-KEY-ID':api_key,
                'X-NCP-APIGW-API-KEY':api_secret
                }
        get_data = requests.get(url, headers = headers) 
        print(get_data.text)
        #{"status":"OK","meta":{"totalCount":722963,"count":5},"places":[{"name":"명동교자 본점","road_address":"서울특별시 중구 명동10길 29","jibun_address":"서울특별시 중구 명동2가 25-2","phone_number":"02-776-5348","x":"126.9856288","y":"37.5625592","distance":988.3559781880206,"sessionId":"-tVeM2gBLhmWpuc11QQ7"},{"name":"필동면옥","road_address":"서울특별시 중구 서애로 26","jibun_address":"서울특별시 중구 필동3가 1-5","phone_number":"02-2266-2611","x":"126.9969235","y":"37.5603727","distance":182.9612384296175,"sessionId":"vMReM2gBe9kwkY1_LGt-"},{"name":"우래옥","road_address":"서울특별시 중구 창경궁로 62-29","jibun_address":"서울특별시 중구 주교동 118-1","phone_number":"02-2265-0151","x":"126.9987029","y":"37.5682698","distance":714.1006604811206,"sessionId":"K8xeM2gBLhmWpuc1M4ec"},{"name":"산수갑산","road_address":"서울특별시 중구 을지로20길 24","jibun_address":"서울특별시 중구 인현동1가 15-4","phone_number":"02-2275-6654","x":"126.9953139","y":"37.5653833","distance":397.09209607324266,"sessionId":"EOheM2gBZphKmN8QVwqa"},{"name":"코너스테이크","road_address":"서울특별시 중구 퇴계로 218-16","jibun_address":"서울특별시 중구 필동2가 28-10 1층","phone_number":"02-6428-2204","x":"126.9963863","y":"37.5608706","distance":133.26563021309497,"sessionId":"5MReM2gBe9kwkY1_MZJQ"}],"errorMessage":""}

        data = json.loads(get_data.text)
        message=''
        for place in data['places']:
            name = place['name']
            address = place['road_address']
            message += f'{name} / {address} \n' 
        print(message)
        return message 
