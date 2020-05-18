import logging
import config as cfg
from concurrent.futures import ThreadPoolExecutor
import datetime
import requests
from bs4 import BeautifulSoup
from random import choice
from Log import main_logger


class ProxyManager:

    def __init__(self):
        self.url_for_test_proxy = cfg.url_for_test_proxy
        self.headers = cfg.random_headers()
        self.thread_pool = ThreadPoolExecutor(max_workers=cfg.thread_pool_workers)
        self.proxy_options = {}
        self.proxies = []

    def get_proxies(self) -> 'list of proxies':
        """отдает список живых прокси,
         если в списке proxies пусто - трясет новый список."""
        while not self.proxies:
            main_logger.debug('в списке proxies[] нет живых. Запрашиваю новый список.')
            self.update_proxies()
        return self.proxies

    def get_random_proxy(self) -> 'proxy':
        """возвращает один случайный прокси из списка proxies вида 123.234.023.12:8080"""
        proxy = choice(self.get_proxies())
        return proxy

    def update_proxies(self) -> None:
        """обновляет статусы прокси, заново ища и тестируя их, оставляет в списке только живые"""
        main_logger.debug('start update_proxies')
        if self.proxy_options == {}:
            self.update_proxies_pretenders()
        self.refresh_proxies_status()
        self.proxies = [proxy for proxy, options in self.proxy_options.items() if options.get('alive')]
        self.proxy_options = {proxy: options for proxy, options in self.proxy_options.items() if options.get('alive')}
        main_logger.debug('update_proxies done %d' % len(self.proxies))

    def update_proxies_pretenders(self):
        """перезаписывает список proxies для тестирования на пригодность"""
        main_logger.debug('start update_proxies_pretenders')
        try:
            proxies = {}
            # sources of proxy list: https://www.free-proxy-list.net/  https://www.socks-proxy.net/
            response = requests.get('https://www.free-proxy-list.net/', headers=self.headers, timeout=(9, 27))

            soup = BeautifulSoup(response.text, 'html.parser')
            proxy_list = soup.select('table#proxylisttable tr')
            for p in proxy_list:
                info = p.find_all('td')
                if len(info):
                    proxy = ':'.join([info[0].text, info[1].text])
                    proxies.update({proxy: {'country_code': info[2].text,
                                            'country': info[3].text,
                                            'privacy': info[4].text,
                                            'google': info[5].text,
                                            'https': info[6].text,
                                            'last_checked': None,
                                            'alive': True,
                                            'detected_ip': 'Not checked yet',
                                            'response_headers': 'Not checked yet'}})
            self.proxy_options = proxies
            # if not proxies:
            #     main_logger.warn('get no proxies in update_proxies_pretenders')
            #     main_logger.warn('bad header - %s' % self.headers)
            #     main_logger.debug('update headers')
            #     self.headers = cfg.random_headers()
            #     main_logger.debug('call update_proxies_pretenders again')
            #     self.update_proxies()
            # else:
            #     main_logger.debug('useful headers - %s' % self.headers)
        except Exception as e:
            logging.error('Unable to update proxy list, exception : {}'.format(e))
        main_logger.debug('update_proxies_pretenders done %d' % len(self.proxy_options))

    def refresh_proxies_status(self) -> 'proxies dict':
        """многопоточно тестирует proxy на пригодность о тестовый url(см.конфиг), возвращает список словарей
        proxies, где key - это прокси вида '123.23.167.10:80', а values - словарь опций info
        тем прокси, которые не прошли тестирования выставляет в ключ 'alive' - False"""
        main_logger.debug('start refresh_proxies_status')

        def __check_proxy_status(proxy, info):
            info['last_checked'] = datetime.datetime.now()
            try:
                headers = cfg.random_headers()
                resp = requests.get(self.url_for_test_proxy,
                                    proxies={'proxyType': 'manual',
                                             'https': proxy,
                                             'socksProxy': proxy,
                                             'socksVersion': 4}, headers=headers, timeout=(4, 8))
                # timeout 4 sec - connect, 8-response
                info['response_headers'] = resp.headers
                info['detected_ip'] = 'Nice!!!'
                resp.raise_for_status()
            except Exception as e:
                info['alive'] = False
                info['response_headers'] = e
                info['detected_ip'] = 'Error!!! Have not response server!'
                # main_logger.error(e)
            else:
                info['alive'] = True
            return {proxy: info}
        with self.thread_pool as tp:
            print(self.proxy_options)
            results = [tp.submit(__check_proxy_status, k, v) for k, v in self.proxy_options.items()]
        for res in results:
            result = res.result()
            self.proxy_options.update(result)
        main_logger.debug('refresh_proxies_status done %d' % len(self.proxy_options))

    def del_proxy(self, proxy) -> None:
        """удаляет proxy из списка proxies, если список опустел, запрашивает его наполнение"""
        self.proxies.pop(proxy)
        if not self.proxies:
            self.get_proxies()


