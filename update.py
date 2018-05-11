from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from sqlalchemy import inspect
from sqlalchemy import desc
from sqlalchemy import and_
import parser

engine = create_engine('postgresql://let4ik:let4ik_password@localhost/news_parser', echo=False)
Base = declarative_base()


document_tag = Table('document_tag', Base.metadata,
                     Column('document_id', ForeignKey('document.id'),
                            primary_key=True),
                     Column('tag_id', ForeignKey('tag.id'),
                            primary_key=True))

theme_document = Table('theme_document', Base.metadata,
                     Column('theme_id', ForeignKey('theme.id'),
                            primary_key=True),
                     Column('document_id', ForeignKey('document.id'),
                            primary_key=True))


class Theme(Base):
    __tablename__ = 'theme'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    text = Column(String)
    documents = relationship('Document', secondary=theme_document,
                             back_populates='themes')

    def __repr__(self):
        return "<Theme(url='%s', title='%s', text='%s')>" %\
               (self.url, self.title, self.text)


class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    text = Column(String)
    upd_time = Column(DateTime)
    themes = relationship('Theme', secondary=theme_document,
                          back_populates='documents')
    tags = relationship('Tag', secondary=document_tag,
                        back_populates='documents')

    def __repr__(self):
        return "<Tag(id='%s', title='%s'')>" %\
               (self.id, self.title)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    documents = relationship('Document', secondary=document_tag,
                             back_populates='tags')

    def __repr__(self):
        return "<Tag(id='%s', text='%s'')>" %\
               (self.id, self.text)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def update_database(themes_number, docs_number):
    i = 1
    for theme_data in parser.get_themes(themes_number, docs_number):
        print('Theme number {} out of {}'.format(i, themes_number))
        print(theme_data['title'])
        i += 1
        theme = session.query(Theme).filter(Theme.url == theme_data['url']).first()
        if not theme:
            theme = Theme(url=theme_data['url'], title=theme_data['title'], text=theme_data['text'])
        for document_data in theme_data['documents_list']:
            document = session.query(Document).filter(Document.url == document_data['url']).first()
            if not document:
                document_data.update(parser.get_document(document_data['url']))
                document = Document(
                    url=document_data['url'], title=document_data['title'],
                    text=document_data['text'],
                    upd_time=document_data['upd_time'])
                for tag_text in document_data['tags']:
                    tag = session.query(Tag).filter(Tag.text == tag_text).first()
                    if not tag:
                        tag = Tag(text=tag_text)
                    session.add(tag)
                    document.tags.append(tag)
            elif document.upd_time != document_data['upd_time']:
                document_data.update(parser.get_document(document_data['url']))
                document.text = document_data['text']
                document.title = document_data['title']
            if document not in theme.documents:
                theme.documents.append(document)
        session.add(theme)
    session.commit()


def new_docs(amount):
    res = session.query(Document).order_by(desc(Document.upd_time))[:amount]
    return res


import time
cur_time = time.time()
update_database(10, 10)
print('Elapsed time : {} seconds'.format(time.time() - cur_time))
