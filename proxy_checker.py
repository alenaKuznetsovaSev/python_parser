from random import choice
import urllib3
import requests
from colorama import Fore,Style

#URL = "https://whatismyipaddress.com/ip-lookup"
URL = "https://api.ipify.org"
CMD_CLEAR_TERM = "clear"
TIMEOUT = (3.05, 27)

agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
          'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

accept = ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
          'text/html,application/xhtml+xml,application/xml;q=0.9,image/png,image/*;q=0.8,*/*;q=0.5',
          '',]

accept_encoding = ['gzip',
                   'gzip,compress,br',
                   'br;q=1.0, gzip;q=0.8, *;q=0.1',
                   '*',
                   'gzip;q=1.0, identity; q=0.5, *;q=0', ]

#здесь лучше опрашивать страну сервера прокси и делать первым энкодинг этой страны
accept_language = ['ru, en-gb',
                   'en-gb',
                   'it, en-gb',
                   'ua, en-gb',
                   'de, en-gb;q=0.8',
                   'en', ]

def random_headers():
    return {'User-Agent': choice(agents),
            'Accept': choice(accept),
            'Accept-Encoding': choice(accept_encoding),
            'Accept-Language': choice(accept_language) }


def check_proxy(proxy):
    '''
        Function for check proxy return ERROR
        if proxy is Bad else
        Function return None
    '''
    try:
        session = requests.Session()
        #session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        session.max_redirects = 300
        proxy = proxy.split('\n', 1)[0]
        print(Fore.LIGHTYELLOW_EX + 'Checking ' + proxy)
        headers = random_headers()
        print('Заголовок: ' + str(headers))
        print('Прокси: ' + proxy)
        s = session.get(URL, headers=headers, proxies={'http': 'http://' + proxy}, timeout=TIMEOUT, allow_redirects=True)
        print(s.headers)
        print(s.text, end='\n\n')
    except requests.exceptions.ConnectionError as e:
        print(Fore.LIGHTRED_EX + 'Error!')
        return e
    except requests.exceptions.ConnectTimeout as e:
        print(Fore.LIGHTRED_EX + 'Error,Timeout!')
        return e
    except requests.exceptions.HTTPError as e:
        print(Fore.LIGHTRED_EX + 'HTTP ERROR!')
        return e
    except requests.exceptions.Timeout as e:
        print(Fore.LIGHTRED_EX + 'Error! Connection Timeout!')
        return e
    except urllib3.exceptions.ProxySchemeUnknown as e:
        print(Fore.LIGHTRED_EX + 'ERROR unkown Proxy Scheme!')
        return e
    except requests.exceptions.TooManyRedirects as e:
        print(Fore.LIGHTRED_EX + 'ERROR! Too many redirects!')
        return e

check_proxy('175.29.164.1:3629')
check_proxy('194.38.123.211:60230')
check_proxy('217.77.171.114:4140')
check_proxy('186.219.96.225:47514')
check_proxy('12.218.209.130:53281')
