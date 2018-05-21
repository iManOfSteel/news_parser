import telebot
import re
import request_handler
import os
import matplotlib
import statistics
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import DEFAULT_MESSAGE_AMOUNT, MAX_MESSAGE_AMOUNT, HELP_MESSAGE


bot = telebot.TeleBot('591316725:AAFGo5dbW_ztZpcotBDOXC_FBhPQsj32hTI')


@bot.message_handler(commands=['start'])
def greetings(message):
    cid = message.chat.id
    bot.send_message(cid, "Hey, how are you?")


@bot.message_handler(commands=['help'])
def help_cmd(message):
    cid = message.chat.id
    bot.send_message(cid, HELP_MESSAGE)


@bot.message_handler(commands=['new_docs'])
def new_docs(message):
    cid = message.chat.id
    arg = re.findall(r'^/new_docs ([0-9]+)', message.text)
    if len(arg) == 0:
        amount = DEFAULT_MESSAGE_AMOUNT
    else:
        amount = min(MAX_MESSAGE_AMOUNT, int(arg[0]))
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
    arg = re.findall(r'^/new_topics ([0-9]+)', message.text)
    if len(arg) == 0:
        amount = DEFAULT_MESSAGE_AMOUNT
    else:
        amount = min(MAX_MESSAGE_AMOUNT, int(arg[0]))
    topics = request_handler.new_topics(amount)
    for topic in topics:
        res = topic.title + '\n' + topic.url
        bot.send_message(cid, res)


@bot.message_handler(commands=['topic'])
def get_topic(message):
    cid = message.chat.id
    arg = re.findall(r'^/topic (.+)', message.text)
    if len(arg) == 0:
        bot.send_message(cid, "Please the enter topic name after /topic")
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
    arg = re.findall(r'^/doc (.+)', message.text)
    if len(arg) == 0:
        bot.send_message(cid, "Please enter the document name after /doc")
        return
    document_title = arg[0]
    try:
        doc_text = request_handler.get_doc(document_title)
        bot.send_message(cid, doc_text)
    except KeyError:
        bot.send_message(cid, "No such document found")


@bot.message_handler(commands=['words'])
def get_words(message):
    cid = message.chat.id
    arg = re.findall(r'^/words (.+)', message.text)
    if len(arg) == 0:
        bot.send_message(cid, "Please enter the topic name after /words")
        return
    topic_name = arg[0]
    try:
        words = request_handler.words(topic_name)
        res = ', '.join(words)
        bot.send_message(cid, res)
    except KeyError:
        bot.send_message(cid, "No such topic found")


def send_distributions(cid, distributions, x_labels, y_labels,
                       x_scales, y_scales, relevant=False):
    """Prints given distributions
    :param cid: int
        chat id
    :param distributions: list
        distributions to send
    :param x_labels, y_labels: list
        axes labels
    :param x_scales, y_scales: list
        axes scales
    """
    for i in range(len(distributions)):
        mean = statistics.mean(distributions[i].values())
        dev = statistics.stdev(distributions[i].values())
        plt.clf()
        distribution = sorted(
            filter(lambda item: (not relevant) or
                                (mean - 3 * dev <= item[1] <= mean + 3 * dev),
                   distributions[i].items()),
            key=lambda item: int(item[0]))
        x, y = zip(*distribution)
        plt.xscale(x_scales[i])
        plt.yscale(y_scales[i])
        plt.bar(x, y)
        plt.xlabel(x_labels[i])
        plt.ylabel(y_labels[i])
        plt.savefig('distribution.png')
        plot = open('distribution.png', 'rb')
        bot.send_photo(cid, plot)
        os.remove('distribution.png')


@bot.message_handler(commands=['describe_doc'])
def describe_doc(message):
    cid = message.chat.id
    arg = re.findall(r'^/describe_doc (.+)', message.text)
    if len(arg) == 0:
        bot.send_message(cid,
                         "Please enter the document name after /describe_doc")
        return
    document_title = arg[0]
    try:
        distributions = request_handler.describe_doc(document_title)
        x_labels = ['Word length', 'Word frequency']
        y_labels = ['Number of words', 'Number of words']
        x_scales = ['linear', 'log']
        y_scales = ['linear', 'log']
        send_distributions(cid, distributions,
                           x_labels, y_labels,
                           x_scales, y_scales, relevant=False)
    except KeyError:
        bot.send_message(cid, "No such document found")


@bot.message_handler(commands=['describe_topic'])
def describe_topic(message):
    cid = message.chat.id
    arg = re.findall(r'^/describe_topic (.+)', message.text)
    if len(arg) == 0:
        bot.send_message(cid,
                         "Please enter the topic name after /describe_topic")
        return
    topic_name = arg[0]
    try:
        docs_number, avg_length, distributions =\
            request_handler.describe_topic(topic_name)
        res = 'There are {} documents in the topic.\n' \
              'Average document length is {}'.format(docs_number, avg_length)
        bot.send_message(cid, res)
        x_labels = ['Word length', 'Word frequency']
        y_labels = ['Number of words', 'Number of words']
        x_scales = ['linear', 'log']
        y_scales = ['linear', 'log']
        send_distributions(cid, distributions,
                           x_labels, y_labels,
                           x_scales, y_scales,
                           relevant=False)
    except KeyError:
        bot.send_message(cid, "No such topic found")


bot.polling()
