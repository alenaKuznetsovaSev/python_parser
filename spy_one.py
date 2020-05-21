from selenium import webdriver
import pickle
from selenium.webdriver.support.ui import Select
from time import sleep
from PIL import Image
from pytesseract import image_to_string
import Log
from selenium.webdriver.common.keys import Keys


class Bot:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1440, 900)
        self.driver.set_page_load_timeout(5)  # seconds
        self.logger = Log.get_logger('bot')

    def take_screenshot(self):
        self.driver.save_screenshot('spy_one_screenshot.png')

    def tel_recogn(self):
        image = Image.open('tel.gif')
        print(image_to_string(image))

    def crop(self, location, size):
        image = Image.open('avito_screenshot.png')

        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        image.crop([x, y, x+width, y+height]).save('tel.gif')
        self.tel_recogn()

    def navigate(self):
        self.logger.debug('start navigate')
        try:
            self.driver.get('http://spys.one/proxys/US/')
        except Exception as ex:
            self.logger.debug('exception')
        # self.driver.implicitly_wait(10) # seconds

        self.logger.debug('driver got http://spys.one/proxys/US/')
        # считываем cookie
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "a+b"))
        cookies = pickle.load(open('cookies.pkl', 'r+b'))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
            # self.logger.debug(cookie)
        self.logger.debug('got cookies')
        sleep(2)
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

        select = Select(self.driver.find_element_by_name("xpp"))
        select.select_by_value('2')  # 1 = 25, 2 = 100, 3 = 200, 4 = 300, 5 = 500

        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        table = self.driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td/table/tbody')
        # proxies = table.find_elements_by_xpath('/tr[4]/td[1]/font')

        half1table = table.find_elements_by_class_name('spy1xx')
        half2table = table.find_elements_by_class_name('spy1x')
        counter = 1
        for line in half1table[1:]:
            # print(line.text)
            proxy = line.find_element_by_xpath('td[1]/font').text
            type = line.find_element_by_xpath('td[2]/font').text
            anon = line.find_element_by_xpath('td[3]/font').text
            replace_mark = line.find_element_by_xpath('td[5]/font') # если в тексте есть вхождение !! - то replase ip
            try:
                is_replace_ip = replace_mark.find_element_by_tag_name('acronym')
                replace_ip = True
            except:
                replace_ip = False

            speed = line.find_element_by_xpath('td[7]/font/table').get_attribute('width')
            uptime = line.find_element_by_xpath('td[8]/font').text
            checked = line.find_element_by_xpath('td[9]/font').text
            print(counter, ' === ', proxy, type, anon, 'speed =', speed, replace_ip, uptime, checked)
            counter +=1

        for line in half1table[1:]:
            # print(line.text)
            proxy = line.find_element_by_xpath('td[1]/font').text
            type = line.find_element_by_xpath('td[2]/font').text
            anon = line.find_element_by_xpath('td[3]/font').text
            replace_mark = line.find_element_by_xpath('td[5]/font') # если в тексте есть вхождение !! - то replase ip
            try:
                is_replace_ip = replace_mark.find_element_by_tag_name('acronym')
                replace_ip = True
            except:
                replace_ip = False

            speed = line.find_element_by_xpath('td[7]/font/table').get_attribute('width')
            uptime = line.find_element_by_xpath('td[8]/font').text
            checked = line.find_element_by_xpath('td[9]/font').text
            print(counter, ' === ', proxy, type, anon, 'speed =', speed, replace_ip, uptime, checked)
            counter +=1

        self.driver.close()
        # sleep(3)
        #self.take_screenshot()

        # image = self.driver.find_element_by_xpath('//div[@class="item-phone-big-number js-item-phone-big-number"]//*')
        # location = image.location   # dict{ 'x':232, 'y':23}
        # size = image.size           # dict { 'width': 34, 'height' : 324}
        # self.crop(location, size)


def main():
    b = Bot()
    b.navigate()


if __name__ == '__main__':
    main()