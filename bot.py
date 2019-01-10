from slacker import Slacker
import configparser

config = configparser.ConfigParser()
config.read('env.json')

token = config['DEFAULT']['TOKEN'] 
