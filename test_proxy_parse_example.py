def test_webdriver2(self):
    import time
    from selenium import webdriver

    # myProxy = "127.0.0.1:9150"
    myProxy = "175.29.164.1:3629"
    ip, port = myProxy.split(":")
    fp = webdriver.FirefoxProfile()
    fp.set_preference('network.proxy.type', 1)
    fp.set_preference('network.proxy.socks', ip)
    fp.set_preference('network.proxy.socks_port', int(port))
    driver = webdriver.Firefox(fp)
    url = 'https://api.ipify.org'
    # url = "http://data.eastmoney.com/hsgtcg/StockHdDetail.aspx?stock=600519&date=2018-06-12/"
    driver.get(url)
    # print(driver.find_element_by_tag_name('table').text)
    print(driver.find_element_by_tag_name('pre').text)
    driver.get('https://check.torproject.org/')
    time.sleep(3)
    driver.quit()

test_webdriver2(self=None)
