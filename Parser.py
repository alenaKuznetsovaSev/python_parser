from abc import ABC, abstractmethod
from Proxy_manager import ProxyManager
from bs4 import BeautifulSoup
import config as cfg
import requests
from Saver import Saver


class Parser(ABC):
    """абстрактный, его потомки собирают информацию со страниц в словари для передачи Saver`y"""
    base_url = ""
    saver = None
    items_count = 0

    def __init__(self, base_url, saver):
        self.base_url = base_url
        self.saver = saver

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

    @staticmethod
    def make_proxy_request(url) -> str:
        pm = ProxyManager()
        proxies = pm.get_proxies()
        headers = cfg.random_headers()
        res = ''
        for proxy in proxies:
            try:
                res = requests.get(url, proxies={'proxyType': 'manual', 'https': proxy, 'socksProxy': proxy,
                                                 'socksVersion': 4}, headers=headers, timeout=(4, 8))
                res.raise_for_status()
                break
            except:
                continue
        print('make_proxy_request to %s done' % url)
        return res.text
