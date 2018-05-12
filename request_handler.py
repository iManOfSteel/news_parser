from database_config import Theme, Document, Tag, get_session
from sqlalchemy import desc

session = get_session()


def new_docs(amount):
    return session.query(Document).order_by(desc(Document.upd_time))[:amount]


def new_topics(amount):
    pass


def topic(topic_name):
    topic = session.query(Theme).filter(Theme.title == topic_name).first()
    if not topic:
        return 'Topic not exists', []
    docs = session.query(Document).filter(Document.in_(topic.documents)).\
        order_by(desc(Document.upd_time))[:5]
    return topic.text, docs

print(topic('Война в Сирии'))
