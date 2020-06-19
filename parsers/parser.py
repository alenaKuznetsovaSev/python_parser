from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import config as cfg
import requests
import log
from main import saver, proxy_manager

class Parser(ABC):
    """абстрактный, его потомки собирают информацию со страниц в словари для передачи Saver`y"""
    base_url = ""
    saver = None
    proxy_manager = None
    items_count = 0
    logger = None

    def __init__(self, base_url):
        self.base_url = base_url
        self.saver = saver
        self.proxy_manager = proxy_manager
        self.logger = log.get_logger(__name__)

    @abstractmethod
    def get_pagination_links(self, url) -> list:
        """generate pagination links like structure in url_site (https://www.tastemade.com/)
            like https://www.tastemade.com/food/page/173 """
        pass

    @abstractmethod
    def get_links_from_one_page(self, url) -> 'super-BeautifulSoup,child-list':
        """return list of links to current items from one catalog page"""
        page_html = self.make_proxy_request(url)
        return BeautifulSoup(page_html, 'lxml')

    @abstractmethod
    def parse_item_page(self, url) -> 'super-BeautifulSoup,child-dict':
        """parse name of item etc."""
        page_html = self.make_proxy_request(url)
        return BeautifulSoup(page_html, 'lxml')

    def add_to_sql_item_links_from_all_site(self) -> 'None':
        """save to SQL all target links to item from each page of site """
        catalogs = self.get_pagination_links(self.base_url)
        numb = 1
        for i in catalogs:
            links = self.get_links_from_one_page(i)
            self.saver.add_list_of_links_to_sql(self.base_url, links)
            self.saver.add_log(self, "%d page of catalog is in SQL" % numb)
            numb += 1
        self.saver.add_log(self, "all links to items were parsed from %s" % self.base_url)

    def make_proxy_request(self, url) -> str:
        """берет случайный прокси из списка proxies и пытается сделать запрос к целевому сайту для парсинга.
        если это не удается - удаляет такой прокси из списка proxies и повторяет снова."""
        self.logger.debug('start make_proxy_request')
        proxy = self.proxy_manager.get_random_proxy()
        headers = cfg.random_headers()

        try:
            res = requests.get(url, proxies={'proxyType': 'manual', 'https': proxy, 'socksProxy': proxy,
                                             'socksVersion': 4}, headers=headers, timeout=(4, 8))
            res.raise_for_status()
            self.logger.debug('make_proxy_request to %s done' % url)
            return res.text
        except Exception as ex:
            # пока запрос не принес результата
            self.logger.error('make_proxy_request exception %s' % proxy)
            self.proxy_manager.del_proxy(proxy)
            return self.make_proxy_request(url)

