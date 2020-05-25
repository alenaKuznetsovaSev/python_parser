# import webdriver
from selenium import webdriver

# import Action chains
from selenium.webdriver.common.action_chains import ActionChains

# create webdriver object
driver = webdriver.Firefox()

# get geeksforgeeks.org
driver.get("https://www.geeksforgeeks.org/")

# create action chain object
action = ActionChains(driver)

# move the cursor
action.move_by_offset(200, 200)

# perform the operation
action.perform()

