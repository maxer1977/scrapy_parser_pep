from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        # Находим все ссылки на PEP.
        pep_urls = response.css('section[id="index-by-category"]').css(
            'tbody').css('a::attr(href)')

        # Перебираем ссылки по одной.
        for pep_link in pep_urls:
            pep_link = urljoin(self.start_urls[0], pep_link.get())

            # Возвращаем response.follow() с вызовом метода parse_pep().
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        # Выбираем строку, содержащую номер и название, и преобразуем её
        # в список.
        title_list = response.css('h1.page-title::text').get().split()

        data = {
            'number': title_list[1],
            'name': ' '.join(title_list[3:]),
            'status': response.css('abbr::text').get()
        }

        # Передаём словарь с данными в конструктор класса.
        yield PepParseItem(data)
