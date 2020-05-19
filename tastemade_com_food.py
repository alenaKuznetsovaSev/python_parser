from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError

import logging
from random import choice
from concurrent.futures import ThreadPoolExecutor
import datetime
import requests
from bs4 import BeautifulSoup
import pprint
from Parser import Parser
import config as cfg
from Saver import Saver
from abc import ABC
import Log
# base_url = 'https://www.tastemade.com/food'
# tables_name = 'links4parse'


class Tastemade_com_food(Parser, ABC):

    def get_pagination_links(self, url) -> list:
        """generate pagination links like structure in url_site (https://www.tastemade.com/)
                    like https://www.tastemade.com/food/page/173 """
        pages = [(url + '/page/' + str(i)) for i in range(1, 3)]
        return pages

    def get_links_from_one_page(self, url) -> list:
        soup = super().get_links_from_one_page(url)
        links = [self.base_url + div.find('a')['href'] for div in
        soup.find('div', class_="containerVideos").find_all('div', class_='box')]
        return links

    def parse_item_page(self, url) -> dict:
        """grab title, slogan, ingredients[], steps of cooking[], image_link and link to video
            #https://www.tastemade.com/videos/spring-rolls-with-sakura-petals
            """
        self.logger.debug('start parse_item_page')
        page_html = self.make_proxy_request(url)
        soup = BeautifulSoup(page_html, 'lxml')
        title = soup.find('h1', class_='white').text
        slogan = soup.find('div', class_='videoDetails').find('p').text
        ingredients_list = [li.text for li in soup.find_all('li', class_='p-ingredient')]
        ingredients = ""
        for step in ingredients_list:
            ingredients += cfg.custom_splitter + step
        steps_cooking_list = [li.text for li in soup.find('div', class_='e-instructions').ul.find_all('li')]
        steps_cooking = ""
        for step in steps_cooking_list:
            steps_cooking += cfg.custom_splitter + step
        photo_links = 'https:' + soup.find('img', class_='u-photo')['src']
        # example image link https://truffle-assets.imgix.net/8238b21d-l.png?auto=compress,format&fm=pjpg&w=1200
        video_link = soup.find('video')['src']
        # example video link
        # https://renditions3-tastemade.akamaized.net/e5d6ceea-spring-rolls-sakura-petals-l/mp4/e5d6ceea-spring-rolls-sakura-petals-l-540-2000-mp4.mp4
        self.items_count += 1
        self.logger.debug('url - %s, item numb. %d ' % (url, self.items_count))
        self.logger.debug('parse_item_page done')
        return {'table_name': 'food_recipe',
                'title': title,
                'slogan': slogan,
                'ingredients': ingredients,
                'steps': steps_cooking,
                'photo_links': photo_links,
                'video_link': video_link,
                'home_url_id': '0'}


# def get_catalog_pages(home_site_page) -> list:
#     """parse from base_url pagination links """
#     proxies = pm.get_alived_proxy()
#     res = requests.get(self.test_url, proxies={'proxyType': 'manual', 'https': proxy, 'socksProxy': proxy,
#                                                'socksVersion': 4}, headers=headers, timeout=(4, 8)).text
#     # timeout 4 sec - connect, 8-response
#     pass

# pprint.pprint(parse_one_item_page('https://www.tastemade.com/videos/spring-rolls-with-sakura-petals'))
