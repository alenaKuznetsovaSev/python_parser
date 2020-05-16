from seleniumwire import webdriver

PROXY = "194.38.123.211:60230"

webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
    "proxyType": "manual",
    "socksProxy": PROXY,
    

}

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.privatebrowsing.autostart", True)
#profile.set_preference("general.useragent.override", "[user-agent string]")

with webdriver.Firefox() as driver:
    # Open URL
    try:
        driver.get("https://ipinfo.info/html/ip_checker.php")
        for request in driver.requests:
            if request.response:
                print(request.path, request.response.status_code, request.response.headers['Content-Type'])
    except Exception as e:
        print('Something wrong! ' + str(e))

