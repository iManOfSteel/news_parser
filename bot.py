import telebot
from telebot import apihelper

# apihelper.proxy = {'https': 'socks5://telegram:telegram@46.22.210.240:1080',
#                    'http': 'socks5://telegram:telegram@46.22.210.240:1080'}
# apihelper.proxy = {'http': 'http://133.18.205.118:3128'}
bot = telebot.TeleBot('591316725:AAFGo5dbW_ztZpcotBDOXC_FBhPQsj32hTI')


help_message = '''\
You can use these commands:
\help - help
\\new_docs <N> - показать N самых свежих новостей
\\new_topics <N> - показать N самых свежих тем
\\topic <topic_name> - показать описание темы и заголовки 5 самых свежих новостей в этой теме
\doc <doc_title> - показать текст документа с заданным заголовком
\words <topic_name> - показать 5 слов, лучше всего характеризующих тему
\describe_doc <doc_title> - вывести статистику по документу. Статистика:
    1) распределение частот слов
    2) распределение длин слов
describe_topic <topic_name> - вывести статистику по теме. Статистика:
    1) количество документов в теме
    2) средняя длина документов
    3) распределение частот слов в рамках всей темы
    4) распределение длин слов в рамках всей темы'''


@bot.message_handler(commands=['start'])
def greetings(message):
    cid = message.chat.id
    bot.send_message(cid, "Hey body, how are you?")


@bot.message_handler(commands=['help'])
def help(message):
    cid = message.chat.id
    bot.send_message(cid, help_message)


bot.polling()
