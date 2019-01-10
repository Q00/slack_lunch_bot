from slacker import Slacker
import json

with open('env.json','r') as f:
    config=json.load(f)

token = config['DEFAULT']['TOKEN'] 
