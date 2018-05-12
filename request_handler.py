import re
import operator
import json
from database_config import Theme, Document, Tag, get_session
from sqlalchemy import desc
from collections import Counter


session = get_session()


def new_docs(amount):
    return session.query(Document).order_by(desc(Document.upd_time))[:amount]


def new_topics(amount):
    return session.query(Theme).order_by(desc(Theme.last_update))[:amount]


def get_topic(topic_name):
    topic = session.query(Theme).filter(Theme.title == topic_name).first()
    if not topic:
        raise KeyError
    return topic.text, topic.documents[:5]


def get_doc(doc_title):
    document = session.query(Document).filter(Document.title == doc_title).first()
    if not document:
        raise KeyError
    return document.text

def words(topic_name):
    topic = session.query(Theme).filter(Theme.title == topic_name).first()
    if not topic:
        raise KeyError
    title_words = []
    for document in topic.documents:
        title_words.extend(re.findall(r'[a-zA-Zа-яА-Я]+', document.title))
    title_words = filter(lambda word: len(word) > 2, title_words)
    words_count = sorted(Counter(title_words).items(),
                         key=operator.itemgetter(1), reverse=True)
    describing_words = list(map(lambda x: x[0], words_count))[:5]
    return describing_words


def describe_doc(doc_title):
    document = session.query(Document).filter(Document.title == doc_title).first()
    if not document:
        raise KeyError
    return Counter(json.loads(document.length_distribution)),\
        Counter(json.loads(document.words_frequency).values())


def describe_topic(topic_name):
    topic = session.query(Theme).filter(Theme.title == topic_name).first()
    if not topic:
        raise KeyError
    docs_number = len(topic.documents)
    total_length = 0
    length_distribution = Counter()
    words_frequency = Counter()
    for document in topic.documents:
        total_length += len(document.text)
        length_distribution += Counter(json.loads(document.length_distribution))
        words_frequency += Counter(json.loads(document.words_frequency))
    avg_length = total_length / docs_number
    return docs_number, avg_length, length_distribution, Counter(words_frequency.values())

