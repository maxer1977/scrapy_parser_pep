import datetime as dt

from scrapy.exceptions import DropItem

from .settings import BASE_DIR, DATE_FORMAT, HEADER


class PepParsePipeline:
    def __init__(self):
        # Словарь для подсчета статусов
        self.items = {}
        # Переменная для Total
        self.total = 0

    def open_spider(self, spider):
        # pytest ругается на отсутствие этого метода
        # поэтому оставил...
        pass

    def process_item(self, item, spider):
        # Проверяем наличие значения статуса в Item
        if item['status'] is None:
            raise DropItem('В Item отсутствует значение статуса!')

        # Считаем количество для каждого статуса.
        if item['status'] in self.items:
            self.items[item['status']] += 1
        else:
            self.items[item['status']] = 1

        self.total += 1

        return item

    def close_spider(self, spider):
        # Определяем директорию для сохранения результатов
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)

        # Получаем текущие дату и время.
        now = dt.datetime.now()

        # Сохраняем текущие дату-время в указанном формате.
        now_formatted = now.strftime(DATE_FORMAT)

        # Собираем имя файла из полученных переменных:
        file_name = f'status_summary_{now_formatted}.csv'

        # Задаем путь к файлу с результатами.
        file_path = results_dir / file_name

        with open(file_path, mode='w', encoding='utf-8') as f:
            # Записываем строки в csv-файл. Колонки разделяются запятой,
            # без пробелов.
            f.write(HEADER)
            for key, value in self.items.items():
                f.write(f'{key}, {value}\n')
            # Запись итоговой строки
            f.write(f'Total,{self.total}\n')
