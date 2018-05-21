import urllib3
import pymorphy2
import datetime
import re
import json
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from collections import Counter
from config import MONTHS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

retry = Retry(connect=1000, backoff_factor=2)
http = urllib3.PoolManager(retries=retry)


def get_items_from_ajax(url, items_number):
    response = http.request('GET', url + '&limit={}'.format(items_number))
    soup = BeautifulSoup(json.loads(response.data)['html'], 'lxml')
    return soup


def get_documents_list(theme_url, docs_number=20):
    result = []
    theme_id = theme_url.split('story/')[1]
    url = 'https://www.rbc.ru/filter/ajax?story={}&offset=0' \
        .format(theme_id)
    soup = get_items_from_ajax(url, docs_number)
    for item in soup.find_all('div', class_='item_story-single'):
        upd_time = item.contents[3].find('span',
                                         class_='item__info').text.strip()
        if len(upd_time) < 6:
            upd_time = str(datetime.datetime.today().date().day) + ' ' + \
                       str(datetime.datetime.today().month) + ', ' + upd_time
        if len(upd_time) <= 13:
            upd_time = upd_time.split(',')[0] + ' ' + \
                       str(datetime.datetime.today().date().year) + ',' + \
                       upd_time.split(',')[1]
        for key, value in MONTHS.items():
            upd_time = upd_time.replace(key, value)
        upd_time = datetime.datetime.strptime(upd_time, '%d %m %Y, %H:%M')
        item = item.contents[1]
        title = item.find('span', class_='item__title').text.strip()
        text = item.find('span', class_='item__text').text.strip()
        link = item.get('href')
        result.append(dict(url=link, title=title, upd_time=upd_time))
    return result


def get_themes(themes_number=7, docs_number=7):
    res = []
    url = 'https://www.rbc.ru/story/filter/ajax?offset=0'
    soup = get_items_from_ajax(url, themes_number)
    for item in soup.find_all('div', class_='item_story'):
        item = item.contents[1]
        title = item.find('span', class_='item__title').text.strip()
        text = item.find('span', class_='item__text').text.strip()
        link = item.get('href')
        res.append(dict(url=link, title=title,
                        text=text, documents_list=
                        get_documents_list(link, docs_number)))
    return res


def get_document_statistics(text):
    morph = pymorphy2.MorphAnalyzer()
    words = re.findall(r'[a-zA-Zа-яА-Я]+', text)
    words = map(lambda word: morph.parse(word)[0].normal_form, words)
    words = filter(lambda word: morph.pase(word)[0].tag.POS == 'NOUN', words)
    length_distribution = json.dumps(
        Counter(map(lambda word: len(word), words)))
    words_frequency = json.dumps(Counter(words))
    return length_distribution, words_frequency


def get_document(url):
    res = http.request('GET', url)
    soup = BeautifulSoup(res.data, 'lxml')
    tags = [x.text for x in soup.find_all('a', class_='article__tags__link')]
    try:
        text = '\n'.join([x.text for x in soup.find(
            'div',
            class_='article__text').find_all('p')])
    except AttributeError:
        text = ''
    length_distribution, words_frequency = get_document_statistics(text)
    return dict(text=text, tags=tags, length_distribution=length_distribution,
                words_frequency=words_frequency)
