# Config file
MONTHS = dict(янв='1', фев='2', мар='3', апр='4', мая='5',
              июн='6', июл='7', авг='8', сен='9', окт='10', ноя='11', дек='12')
THEMES_TO_PARSE = 10
DOCUMENTS_TO_PARSE = 10
DEFAULT_MESSAGE_AMOUNT = 5
MAX_MESSAGE_AMOUNT = 30
HELP_MESSAGE = '''\
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
