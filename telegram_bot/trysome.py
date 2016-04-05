__author__ = 'bigbrother'



TOKEN = '212618680:AAGkNPQbTYFEjE5Y4SuH6d3JoduIOaajf_4'
OW_TOKEN = '835438bebadf734596dcee00ec70419f'
CITYLIST = 'city.list.json'
URL = 'http://api.openweathermap.org/data/2.5/forecast'
import logging
import json
import requests
from telegram.ext import Updater
from collections import defaultdict
import time


cities = defaultdict(list)

def get_json(b):
    args = {}
    args["id"] = b[1]
    args["appid"] = OW_TOKEN
    r = requests.get(URL, params = args)
    return r.json()



def compose_choice(a):
    ret = "There are several ps:\n"
    for i in a:
        ret += "in " +  str(i[0]) + ";\n"
    return ret + "Specify country: <cityname> <number for variant>\n"

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Bot to lookup the weather.\nGive me the cityname.\n')

def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Request: Moscow\nAnswer: Date: 2016-04-05 18:00:00, Max Temp: -0.7, Min Temp -5.0')

def city(bot, update):
        try:
            st = update.message.text.lower()
            st2 = st.split(sep = " ")
            num = len(st2)
            if st2[0] in cities:
                a = cities[st2[0]]
                if a.__len__() == 1:
                    bot.sendMessage(chat_id=update.message.chat_id, text ='City is found and it is in ' + str(a[0][0]) + '\n')
                    c = get_json(a[0])
                    compose = "Date: " + c['list'][0]['dt_txt'] + ", Max Temp: " + str(c['list'][0]['main']['temp_max'] - 273) + ", Min Temp " + str(c['list'][0]['main']['temp_min'] - 273)
                    bot.sendMessage(chat_id=update.message.chat_id, text = compose)
                else:
                    if(num == 1):
                        bot.sendMessage(chat_id=update.message.chat_id, text = compose_choice(a))
                    else:
                        c = get_json(a[int(st2[1])-1])
                        compose = "Date: " + c['list'][0]['dt_txt'] + ", Max Temp: " + str(c['list'][0]['main']['temp_max'] - 273) + ", Min Temp " + str(c['list'][0]['main']['temp_min'] - 273)
                        bot.sendMessage(chat_id=update.message.chat_id, text = compose)
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text ='City is not found\n')
        except:
            bot.sendMessage(chat_id=update.message.chat_id, text ='Ooooops somthings gone wrong\n')


def init_citylist():
    f = open(CITYLIST,encoding = 'utf-8')
    for i in f.readlines():
        tcity = json.loads(i)
        cities[tcity["name"].lower()].append((tcity['country'], tcity['_id']))

init_citylist()
history_l = 0
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
dispatcher.addTelegramCommandHandler('start', start)
dispatcher.addTelegramCommandHandler('help', help)
dispatcher.addTelegramMessageHandler(city)
updater.start_polling()