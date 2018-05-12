import telebot
from telebot import apihelper

# apihelper.proxy = {'https': 'socks5://telegram:telegram@46.22.210.240:1080',
#                    'http': 'socks5://telegram:telegram@46.22.210.240:1080'}
# apihelper.proxy = {'http': 'http://133.18.205.118:3128'}
bot = telebot.TeleBot('591316725:AAFGo5dbW_ztZpcotBDOXC_FBhPQsj32hTI')


@bot.message_handler(commands=['start'])
def greetings(message):
    bot.reply_to(message, "Hey body, how are you")


bot.polling()
