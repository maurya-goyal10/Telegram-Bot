import logging
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,Dispatcher,CallbackContext
from telegram import ReplyKeyboardMarkup
from flask import Flask,request
from telegram import Update,Bot
import requests 
import json

#enabling logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '2146854676:AAH9A5Jm9dEiMTIzMWdqlt4F_yvV7sQiBKk'
key = 'dd69b939aa0d41bfb2650037038d2b24'
list = [['send_news business','send_news entertainment'],['send_news general','send_news health'],['send_news science','send_news sports'],['send_news technology']]

app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello!!'

@app.route(f'/{TOKEN}',methods = ['GET','POST'])
def webhook():
    update = Update.de_json(request.get_json(),bot)
    dp.process_update(update)
    return "ok"

def start(bot,update):
    print(update)
    author = update.message.from_user.first_name
    reply = f'Hi! {author} \n Welcome to the service of this echo bot created by Maurya Goyal \nuse'
    reply = reply + f'"send_news cat" to send news of a specific category where category can be: \n'
    reply = reply + f'business\nentertainment\ngeneral\nhealth\nscience\nsports\ntechnology'
    bot.send_message(chat_id = update.message.chat.id,text = reply)

def _help(bot,update):
    help_txt = 'If any malfunction contact Maurya Goyal '
    bot.send_message(chat_id = update.message.chat.id,text = help_txt)

def news(bot,update):
    bot.send_message(chat_id = update.message.chat.id, text = 'Choose a category for the news:',
    reply_markup=ReplyKeyboardMarkup(keyboard= list, one_time_keyboard = True))

def echo_text(bot,update):
    reply = update.message.text
    if(reply.lower().split(' ')[0] == 'send_news'):
        bot.send_message(chat_id = update.message.chat.id,text = 'fetching the news')
        cat = reply.lower().split(' ')[1].replace(" ",'')
        if cat not in ['business','entertainment','general','health','science','sports','technology'] :
            bot.send_message(chat_id = update.message.chat.id,text = 'please send a valid category')
        else:
            params = {
                'apiKey': key,
                'country': 'us',
                'category': cat,
                'pageSize': 5
            }
            res = requests.get('https://newsapi.org/v2/top-headlines?',params = params).content
            json_res = json.loads(res)
            for i in json_res['articles']:
                reply = i['title'] + '\n' + i['url']
                bot.send_message(chat_id = update.message.chat.id,text = reply)
    else :
        url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"
        querystring = {"bid":"178","key":"sX5A2PcYZbsN5EY6","uid":update.message.from_user.first_name,"msg":update.message.text}
        headers = {
            'x-rapidapi-host': "acobot-brainshop-ai-v1.p.rapidapi.com",
            'x-rapidapi-key': "b62c424c07mshb6a14119c9fc6ddp1cf5d5jsn2ec41d98fdfa"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = json.loads(response.text)
        response = response["cnt"]
        bot.send_message(chat_id = update.message.chat.id,text = response)

def echo_sticker(bot,update):
    reply_sticker = update.message.sticker.file_id
    bot.sendSticker(chat_id = update.message.chat.id,sticker = reply_sticker)

def error(bot,update):
    logger.error("update '%s' caused error '%s' ",update,update.error)

print('hi!')
bot = Bot(TOKEN)
try:
    bot.set_webhook("https://telegram-bot-maurya.herokuapp.com/"+TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot,None,use_context=False)

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(CommandHandler("news",news))
dp.add_handler(MessageHandler(Filters.text,echo_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_error_handler(error)

if __name__ == '__main__':
    # can't put the dispatcher code here anymore as due to gunicorn it will run this file and hence the condn
    # won't be met __name__ != '__main__' so we just include running on port 8443 inside here 
    app.run(port=8443)