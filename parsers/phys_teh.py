import requests
from main import saver

from bs4 import BeautifulSoup
from parsers.parser import Parser
from abc import ABC


class PhysTeh(Parser, ABC):

    def get_pagination_links(self, url) -> list:
          pass

    def get_links_from_one_page(self, url) -> list:
        pass

    def parse_item_page(self, url) -> dict:
        """забирает имя и степень участника и записывает их в csv-файл
        примерная ссылка -> 'https://olymp.mipt.ru/olympiad/math2018'"""
        self.logger.debug('start parse_item_page')
        page_html = requests.get(url).text
        soup = BeautifulSoup(page_html, 'lxml')
        tables = soup.find_all('table')
        class_numb = 9
        for table in tables:
            trs = table.find('tbody').find_all('tr')
            for i in trs:
                td = i.find_all('td')
                data = [td[0].text, td[2].text]
                saver.write_row_in_file("math2018_%02d.csv" % class_numb, data)
            class_numb += 1
        self.logger.debug('url - %s, item numb. %d ' % (url, self.items_count))
        self.logger.debug('parse_item_page done')
