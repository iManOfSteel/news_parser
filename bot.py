import telebot
import re
import request_handler
from telebot import apihelper

# apihelper.proxy = {'https': 'socks5://telegram:telegram@46.22.210.240:1080',
#                    'http': 'socks5://telegram:telegram@46.22.210.240:1080'}
# apihelper.proxy = {'http': 'http://133.18.205.118:3128'}
bot = telebot.TeleBot('591316725:AAFGo5dbW_ztZpcotBDOXC_FBhPQsj32hTI')


help_message = '''\
You can use these commands:
/help - help
/new_docs <N> - показать N самых свежих новостей
/new_topics <N> - показать N самых свежих тем
/topic <topic_name> - показать описание темы и заголовки 5 самых свежих новостей в этой теме
/doc <doc_title> - показать текст документа с заданным заголовком
/words <topic_name> - показать 5 слов, лучше всего характеризующих тему
/describe_doc <doc_title> - вывести статистику по документу. Статистика:
    1) распределение частот слов
    2) распределение длин слов
/describe_topic <topic_name> - вывести статистику по теме. Статистика:
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


@bot.message_handler(commands=['new_docs'])
def new_docs(message):
    cid = message.chat.id
    arg = re.findall(r'/new_docs ([0-9]+)', message.text)
    if len(arg) == 0:
        bot.send_message(cid, "Please enter number of news to show")
        return
    amount = int(arg[0])
    docs = request_handler.new_docs(amount)
    for doc in docs:
        res = ''
        res += doc.title + '\n'
        res += doc.url + '\n'
        res += '\n'
        bot.send_message(cid, res)


@bot.message_handler(commands=['new_topics'])
def new_topics(message):
    cid = message.chat.id
    arg = re.findall(r'/new_topics ([0-9]+)', message.text)
    if len(arg) == 0:
        bot.send_message(cid, "Please enter number of topics to show")
        return
    amount = int(arg[0])
    topics = request_handler.new_topics(amount)
    for topic in topics:
        res = topic.title + '\n' + topic.url
        bot.send_message(cid, res)


@bot.message_handler(commands=['topic'])
def get_topic(message):
    cid = message.chat.id
    arg = re.findall(r'/topic (.+)', message.text)
    if len(arg) == 0:
        bot.send_message(cid, "Please enter topic name")
        return
    topic_name = arg[0]
    try:
        topic_text, documents = request_handler.get_topic(topic_name)
    except KeyError:
        bot.send_message(cid, "No such topic found")
        return
    bot.send_message(cid, topic_text)
    for document in documents:
        res = document.title + '\n' + document.url
        bot.send_message(cid, res)


@bot.message_handler(commands=['doc'])
def get_doc(message):
    cid = message.chat.id
    arg = re.findall(r'/doc (.+)', message.text)
    if len(arg) == 0:
        bot.send_message(cid, "Please enter document name")
        return
    document_title = arg[0]
    try:
        doc_text = request_handler.get_doc(document_title)
        bot.send_message(cid, doc_text)
    except KeyError:
        bot.send_message(cid, "No such document found")


bot.polling()
