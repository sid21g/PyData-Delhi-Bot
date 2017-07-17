from telegram.ext import Updater,CommandHandler
from telegram import ChatAction
from datetime import datetime, timedelta
from pytz import timezone
from time import sleep
import logging,requests,pytz,re,ast

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater=Updater(token='<Bot-Token>')
dispatcher=updater.dispatcher

meetupApi={'sign':'true','key':'<Meetup-API-Key>'}

utc = pytz.utc

print("I'm On..!!")

def start(bot, update, args):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='''
Hi! My powers are solely for the service of PyData Delhi Community
Use /help to get /help''')

def website(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://pydatadelhi.github.io/ (WIP)')

def twitter(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='http://twitter.com/pydatadelhi')

def meetup(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://www.meetup.com/PyDataDelhi/')

def nextmeetup(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        r=requests.get('http://api.meetup.com/PyDataDelhi/events', params=meetupApi)
        #print(r.json()[0])
        event_link=r.json()[0]['link']
        date_time=r.json()[0]['time']//1000
        utc_dt = utc.localize(datetime.utcfromtimestamp(date_time))
        indian_tz = timezone('Asia/Kolkata')
        date_time=utc_dt.astimezone(indian_tz)
        date_time=date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        if 'venue' in r.json()[0]:
                venue=r.json()[0]['venue']['address_1']
                bot.sendLocation(chat_id=update.message.chat_id, latitude=r.json()[0]['venue']['lat'],longitude=r.json()[0]['venue']['lon'])
        else:
                venue='Venue is still to be decided'
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup
Date/Time : %s
Venue : %s
Event Page : %s
'''%(date_time, venue, event_link))

def nextmeetups(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        r=requests.get('http://api.meetup.com/PyDataDelhi/events', params=meetupApi)
        #print(re.sub('</a>','',re.sub('<a href="','',re.sub('<br/>',' ',re.sub('<p>',' ',re.sub('</p>','\n',r.json()[0]['description']))))))
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup Schedule
%s
'''%(re.sub('</a>','',re.sub('<a href="','',re.sub('<br/>',' ',re.sub('<p>',' ',re.sub('</p>','\n',r.json()[0]['description'])))))),parse_mode='HTML')

def facebook(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://www.facebook.com/pydatadelhi')

def github(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://github.com/pydatadelhi')

def invitelink(bot,update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://t.me/joinchat/B71pNUGrUQ7QHuyUJq-Ajg')

def help(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id, text='''
Use one of the following commands
/twitter - to get PyData Delhi Twitter link
/meetuppage - to get a link to PyData Delhi Meetup page
/nextmeetup - to get info about next Meetup
/nextmeetupschedule - to get schedule of next Meetup
/facebook - to get a link to PyData Delhi Facebook page
/github - to get a link to PyData Delhi Github page
/website - to get the website of PyData Delhi
/invitelink - to get an invite link for PyData Delhi Telegram Group of Volunteers
/help - to see recursion in action ;)

To contribute to|modify this bot : https://github.com/realslimshanky/PyData-Delhi-Bot
''')

dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
dispatcher.add_handler(CommandHandler('website', website))
dispatcher.add_handler(CommandHandler('twitter', twitter))
dispatcher.add_handler(CommandHandler('meetuppage', meetup))
dispatcher.add_handler(CommandHandler('nextmeetup', nextmeetup))
dispatcher.add_handler(CommandHandler('nextmeetupschedule', nextmeetups))
dispatcher.add_handler(CommandHandler('facebook', facebook))
dispatcher.add_handler(CommandHandler('github', github))
dispatcher.add_handler(CommandHandler('invitelink', invitelink))
dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
