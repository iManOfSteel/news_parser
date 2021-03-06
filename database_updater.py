from database_config import Theme, Document, Tag, get_session
import parser
from datetime import datetime
from config import DOCUMENTS_TO_PARSE, THEMES_TO_PARSE
import sys


def update_database(themes_number, docs_number):
    """Updates database. Parses site looking for new docs/topics"""
    session = get_session()
    i = 1
    for theme_data in parser.get_themes(themes_number, docs_number):
        print('Theme number {} out of {}'.format(i, themes_number))
        print(theme_data['title'])
        i += 1
        theme = session.query(Theme).\
            filter(Theme.url == theme_data['url']).first()
        if not theme:
            theme = Theme(url=theme_data['url'], title=theme_data['title'],
                          text=theme_data['text'], last_update=datetime.min)
        for document_data in theme_data['documents_list']:
            document = session.query(Document).\
                filter(Document.url == document_data['url']).first()
            if not document:
                document_data.update(parser.get_document(document_data['url']))
                document = Document(
                    url=document_data['url'], title=document_data['title'],
                    text=document_data['text'],
                    upd_time=document_data['upd_time'],
                    length_distribution=document_data['length_distribution'],
                    words_frequency=document_data['words_frequency'])
                for tag_text in document_data['tags']:
                    tag = session.query(Tag).\
                        filter(Tag.text == tag_text).first()
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
            theme.last_update = max(theme.last_update, document.upd_time)
        session.add(theme)
    session.commit()


if __name__ == '__main__':
    while True:
        update_database(THEMES_TO_PARSE, DOCUMENTS_TO_PARSE)
