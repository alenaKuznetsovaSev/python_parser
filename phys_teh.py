import config as cfg
import requests
import Log
from bs4 import BeautifulSoup
from Proxy_manager import ProxyManager
from Saver import Saver
from DBcm import UseDatabase

logger = Log.get_logger("phys teh")
proxy_manager = ProxyManager()
logger.info('program started')


# def make_proxy_request(url) -> str:
#     """берет случайный прокси из списка proxies и пытается сделать запрос к целевому сайту для парсинга.
#     если это не удается - удаляет такой прокси из списка proxies и повторяет снова."""
#     logger.debug('start make_proxy_request')
#     proxy = proxy_manager.get_random_proxy()
#     headers = cfg.random_headers()
#
#     try:
#         res = requests.get(url, proxies={'proxyType': 'manual', 'https': proxy, 'socksProxy': proxy,
#                                          'socksVersion': 4}, headers=headers, timeout=(4, 8))
#         res.raise_for_status()
#         logger.debug('make_proxy_request to %s done' % url)
#         return res.text
#     except Exception as ex:
#         # пока запрос не принес результата
#         logger.error('make_proxy_request exception %s' % proxy)
#         proxy_manager.del_proxy(proxy)
#         return make_proxy_request(url)

with UseDatabase(cfg.dbconfig) as cursor:
    saver = Saver(cursor)
    page_html = requests.get('https://olymp.mipt.ru/olympiad/math2018').text
    soup = BeautifulSoup(page_html, 'lxml')
    tables = soup.find_all('table')
    numb = 9
    for table in tables:
        trs = table.find('tbody').find_all('tr')
        for i in trs:
            td = i.find_all('td')
            data = [td[0].text, td[2].text]
            saver.write_row_in_file("math2018_%02d.csv" % numb, data)
        numb += 1