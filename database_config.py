from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table


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
    last_update = Column(DateTime)
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
    length_distribution = Column(String)
    words_frequency = Column(String)
    themes = relationship('Theme', secondary=theme_document,
                          back_populates='documents')
    tags = relationship('Tag', secondary=document_tag,
                        back_populates='documents')

    def __repr__(self):
        return "<Document(id='%s', title='%s'')>" %\
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


def get_session():
    engine = create_engine(
        'postgresql://let4ik:let4ik_password@localhost/news_parser',
        echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
