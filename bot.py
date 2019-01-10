from slacker import Slacker
import json

with open('env.json','r') as f:
    config=json.load(f)

token = config['DEFAULT']['OAUTH_TOKEN'] 
slack = Slacker(token)
slack.chat.post_message('#random','test!')
