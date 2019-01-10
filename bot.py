from slacker import Slacker
import json
import time 
import websocket
import bot_class

def create_bot():

    with open('env.json','r') as f:
        config=json.load(f)
    token = config['DEFAULT']['OAUTH_TOKEN'] 
    slacker = Slacker(token)
    #slack.chat.post_message('#random','test!')
    print(slacker)
    return bot_class.Bot(slacker, config)

def run():
    bot = create_bot()
    bot.loop()
if __name__=="__main__":
    run()

