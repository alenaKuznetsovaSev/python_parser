import os

from selenium import webdriver
import pickle

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from time import sleep
from PIL import Image
from pytesseract import image_to_string
import Log
from selenium.webdriver.common.keys import Keys

from DBcm import UseDatabase
from Saver import Saver
import config as cfg
import random


class Bot:

    monitor_width = 1920
    monitor_height = 1080

    def __init__(self, saver):

        profile = webdriver.FirefoxProfile(os.path.expanduser('~/.mozilla/firefox/jpdh0zw6.default-release'))

        # PROXY_HOST = "12.12.12.123"
        # PROXY_PORT = "1234"
        # profile.set_preference("network.proxy.type", 1)
        # profile.set_preference("network.proxy.http", PROXY_HOST)
        # profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
        profile.set_preference('dom.webdriver.enabled', False)
        profile.set_preference('useAutomationExtension', False)
        profile.set_preference('acceptInsecureCerts', True)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        desired['marionette'] = True

        self. driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired)

        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(self.monitor_width, self.monitor_height)
        self.driver.set_page_load_timeout(5)  # seconds
        self.logger = Log.get_logger('bot')
        self.saver = saver

    def take_screenshot(self):
        """Записывает скнишок экрана
        # image = self.driver.find_element_by_xpath('//div[@class="item-phone-big-number js-item-phone-big-number"]//*')
        # location = image.location   # dict{ 'x':232, 'y':23}
        # size = image.size           # dict { 'width': 34, 'height' : 324}
        # self.crop(location, size)"""
        self.driver.save_screenshot('spy_one_screenshot.png')

    def tel_recogn(self):
        """распознаем телефон на картинке"""
        image = Image.open('tel.gif')
        print(image_to_string(image))

    def crop(self, location, size) -> bool:
        """вырезаем кртинку с телефоном из всплывающего окна avito и помещаем ее в tel.gif"""
        image = None
        try:
            image = Image.open('avito_screenshot.png')
        except Exception as e:
            self.logger.error('"avito_screenshot.png" not find', e)
            return False
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        image.crop([x, y, x+width, y+height]).save('tel.gif')
        return True

    def get_cookies(self):
        """считываем cookie из файла cookies.pkl или выходим с ошибкой"""
        cookies = []
        try:
            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "a+b"))
            cookies = pickle.load(open('cookies.pkl', 'r+b'))
        except Exception as e:
            self.logger.error('Cookies file "cookie.pkl" not find', e)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
            # self.logger.debug(cookie)
        self.logger.debug('got cookies')

    def mouse_moving_like_user(self):
        self.logger.debug('start mouse_moving_like_user')
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

        # пример выполнения javascript  по прокручиванию страницы на webdriver
        # last_height = self.driver.execute_script("return document.body.scrollHeight")
        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # устанавливаем начальную позицию курсора
        start_mouse_location_x = random.randint(20, self.monitor_width)
        start_mouse_location_y = random.randint(20, self.monitor_height)
        print(start_mouse_location_x, start_mouse_location_y)
        webdriver.ActionChains(self.driver).move_by_offset(xoffset=start_mouse_location_x,
                                              yoffset=start_mouse_location_y).perform()
        self.logger.debug('set cursor to random position done')

        # получаем положение селектора количества записей на странице и перемещаемся к нему
        select_element = self.driver.find_element_by_name('xpp')
        # {'x': 935, 'y': 233} - положение селектора
        print(select_element.location)
        webdriver.ActionChains(self.driver).move_to_element(select_element).perform()
        self.logger.debug('set cursor to selector position done')

        # еще полезные методы
        # .move_to_element_with_offset(select, xoffset=3, yoffset=4)
        # .move_to_element_with_offset(to_element, xoffset, yoffset)
        # .move_to_element(element)
        # .perform()
        # .reset_actions()

    def choose_more_lines(self):
        """выбирает с помощью селектора количество выводимых Ajax записей"""
        select = Select(self.driver.find_element_by_name("xpp"))
        select.select_by_value('5')  # 1 = 25, 2 = 100, 3 = 200, 4 = 300, 5 = 500
        sleep(1)
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def parse_result_table(self):
        """разбирает полученную таблицу на поля и отдает сейверу значения для записи"""
        table = self.driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td/table/tbody')
        # proxies = table.find_elements_by_xpath('/tr[4]/td[1]/font')

        half1table = table.find_elements_by_class_name('spy1xx')
        half2table = table.find_elements_by_class_name('spy1x')
        table = [half1table, half2table]
        counter = 1
        for i in table:
            for line in i[1:]:
                # print(line.text)
                proxy = line.find_element_by_xpath('td[1]/font').text
                type_proxy = line.find_element_by_xpath('td[2]/font').text
                anon = line.find_element_by_xpath('td[3]/font').text
                replace_mark = line.find_element_by_xpath('td[5]/font') # если в тексте есть вхождение !! - то replase ip
                try:
                    is_replace_ip = replace_mark.find_element_by_tag_name('acronym')
                    replace_ip = True
                except Exception as ex:
                    replace_ip = False

                speed = int(line.find_element_by_xpath('td[7]/font/table').get_attribute('width'))
                uptime = line.find_element_by_xpath('td[8]/font').text
                checked = line.find_element_by_xpath('td[9]/font').text
                self.logger.debug('%03d === %s, %s, %s speed = %d, %s, %s, %s' % (
                counter, proxy, type_proxy, anon, speed, replace_ip, uptime, checked))
                try:
                    check_count = int(uptime.split('(')[1].split(')')[0])
                    check_count = int(check_count * 100 / int(uptime.split('%')[0]))
                    success_checks = int(uptime.split('(')[1].split(')')[0])
                except Exception as ex:
                    check_count = 1
                    success_checks = 1
                self.saver.add_item_content_to_sql({'table_name': 'proxies',
                                                    'proxy': proxy,
                                                    'type': type_proxy,
                                                    'replace_ip': 1 if replace_ip else 0,
                                                    'speed': speed,
                                                    'check_count': check_count,
                                                    'success_checks': success_checks,
                                                    'alive': 1})
                counter += 1
                # breakpoint()
                counter += 1

    def navigate(self):
        """задает последовательность действий для парсинга"""
        self.logger.debug('start navigate')
        target_url = 'http://spys.one/proxys/BR/'  # http://spys.one/proxys/DE/
        try:
            self.driver.get(target_url)
        except Exception as e:
            self.logger.error('Have\'t got %s' % target_url)
            self.logger.error(e)
        self.logger.debug('driver got %s' % target_url)

        # необязательный метод, записывает куки
        # self.get_cookies()

        # необязательный метод, только двигает курсором, но ничего не нажимает
        # self.mouse_moving_like_user()

        # выбирает сколько записей вывести
        self.choose_more_lines()

        self.parse_result_table()

        self.driver.close()
        # sleep(3)
        #self.take_screenshot()




def main():
    with UseDatabase(cfg.dbconfig) as cursor:
        saver = Saver(cursor)
        b = Bot(saver)
        b.navigate()


if __name__ == '__main__':
    main()
