from pathlib import Path

BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

BASE_DIR = Path(__file__).parent.parent
DATE_FORMAT = "%Y-%m-%dT%H-%M-%S"
HEADER = 'Статус,Количество\n'

ROBOTSTXT_OBEY = True

FEEDS = {
    # Директория и имя файла для сохранения данных
    'results/pep_%(time)s.csv': {
        # Формат файла.
        'format': 'csv',
        # Поля, данные из которых будут выведены в файл, и их порядок.
        'fields': ['number', 'name', 'status'],
        # Если файл с заданным именем уже существует, то
        # существующий файл будет перезаписан.
        'overwrite': True
    },
}

ITEM_PIPELINES = {
    # Активация PepParsePipeline
    'pep_parse.pipelines.PepParsePipeline': 300,
}
