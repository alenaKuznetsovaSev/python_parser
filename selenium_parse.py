from selenium import webdriver
from time import sleep
from PIL import Image
from pytesseract import image_to_string
class Bot:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.navigate()

    def take_screenshot(self):
        self.driver.save_screenshot('avito_screenshot.png')

    def tel_recogn(self):
        image = Image.open('results/tel.gif')
        print(image_to_string(image))

    def crop(self, location, size):
        image = Image.open('results/avito_screenshot.png')

        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        image.crop([x, y, x+width, y+height]).save('tel.gif')
        self.tel_recogn()

    def navigate(self):
        list_of_flats = 'https://www.avito.ru/sevastopol/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?f=ASgBAQICAkSSA8gQ8AeQUgFAzAg0jFmQWY5Z'
        self.driver.get('https://www.avito.ru/sevastopol/kvartiry/studiya_23_m_19_et._1162753384')
        button = self.driver.find_element_by_xpath('//a[@class="button item-phone-button js-item-phone-button button-origin contactBar_greenColor button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card contactBar_height"]')
        button.click()
        sleep(3)
        self.take_screenshot()

        image = self.driver.find_element_by_xpath('//div[@class="item-phone-big-number js-item-phone-big-number"]//*')
        location = image.location   # dict{ 'x':232, 'y':23}
        size = image.size           # dict { 'width': 34, 'height' : 324}
        self.crop(location, size)


def main():
    b = Bot()


if __name__ == '__main__':
    main()