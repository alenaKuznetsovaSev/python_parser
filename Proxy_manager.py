import logging
import config as cfg
from concurrent.futures import ThreadPoolExecutor
import datetime
import requests
from bs4 import BeautifulSoup


class ProxyManager:

    def __init__(self):
        self.url_for_test_proxy = cfg.url_for_test_proxy
        self.headers = cfg.random_headers()
        self.thread_pool = ThreadPoolExecutor(max_workers=cfg.thread_pool_workers)
        self.proxy_options = {}
        self.proxies = []

    def get_proxies(self) -> 'list of proxies':
        self.update_proxies()
        while self.proxies == []:
            print('self.proxies == []')
            self.update_proxies()
        return self.proxies

    def update_proxies(self) -> list:
        """обновляет статусы прокси, заново ища и тестиря их"""
        if self.proxy_options == {}:
            self.update_proxies_pretenders()
        self.refresh_proxies_status()
        self.proxies = [proxy for proxy, options in self.proxy_options.items() if options.get('alive')]
        self.proxy_options = {proxy: options for proxy, options in self.proxy_options.items() if options.get('alive')}
        print('update_proxies done')

    def update_proxies_pretenders(self):
        """перезаписывает список proxies для тестирования на пригодность"""
        try:
            proxies = {}
            # sources of proxylist: https://www.free-proxy-list.net/  https://www.socks-proxy.net/
            response = requests.get('https://www.free-proxy-list.net/', headers=self.headers, timeout=(9, 27))
            soup = BeautifulSoup(response.text, 'html.parser')
            proxy_list = soup.select('table#proxylisttable tr')
            for p in proxy_list:
                info = p.find_all('td')
                if len(info):
                    proxy = ':'.join([info[0].text, info[1].text])
                    proxies.update({proxy: {'country_code': info[2].text, 'country': info[3].text, 'privacy': info[4].text,
                                            'google': info[5].text, 'https': info[6].text, 'last_checked': None,
                                            'alive': True, 'detected_ip': 'Not checked yet',
                                            'response_headers': 'Not checked yet'}})
            self.proxy_options = proxies
        except Exception as e:
            logging.error('Unable to update proxy list, exception : {}'.format(e))
        print('update_proxies_pretenders done')

    def refresh_proxies_status(self):
        """тестирует proxy на пригодность"""
        def __check_proxy_status(proxy, info):
            info['last_checked'] = datetime.datetime.now()
            try:
                headers = cfg.random_headers()
                res = requests.get(self.url_for_test_proxy, proxies={'proxyType': 'manual', 'https': proxy, 'socksProxy': proxy,
                                                           'socksVersion': 4}, headers=headers, timeout=(4, 8))
                # timeout 4 sec - connect, 8-response
                info['response_headers'] = res.headers
                info['detected_ip'] = 'Nice!!!'
                res.raise_for_status()
            except Exception as e:
                info['alive'] = False
                info['response_headers'] = e
                info['detected_ip'] = 'Error!!! Have not response server!'
                # print(e)
            else:
                info['alive'] = True
            return {proxy: info}
        with self.thread_pool as tp:
            results = [tp.submit(__check_proxy_status, k, v) for k, v in self.proxy_options.items()]
        for res in results:
            result = res.result()
            self.proxy_options.update(result)
        print('refresh_proxies_status done')
