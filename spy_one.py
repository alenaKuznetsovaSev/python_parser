from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from PIL import Image
from pytesseract import image_to_string


class Bot:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.navigate()

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
        self.driver.get('http://spys.one/proxys/US/')
        select = Select(self.driver.find_element_by_name("xpp"))
        select.select_by_value('3') # 1 = 25, 2 = 100, 3 = 200, 4 = 300, 5 = 500
        table = self.driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td')

        print(table.text)


        # <tr class ="spy1xx" onmouseover="this.style.background='#002424'" onmouseout="this.style.background='#003333'" style="background: rgb(0, 51, 51) none repeat scroll 0% 0%;" >
        # <tr class="spy1x" onmouseover="this.style.background='#002424'" onmouseout="this.style.background='#19373A'" style="background: rgb(25, 55, 58) none repeat scroll 0% 0%;">
        sleep(3)
        #self.take_screenshot()

        # image = self.driver.find_element_by_xpath('//div[@class="item-phone-big-number js-item-phone-big-number"]//*')
        # location = image.location   # dict{ 'x':232, 'y':23}
        # size = image.size           # dict { 'width': 34, 'height' : 324}
        # self.crop(location, size)


def main():
    b = Bot()


if __name__ == '__main__':
    main()