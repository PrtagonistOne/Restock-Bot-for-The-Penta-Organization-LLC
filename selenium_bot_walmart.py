import random
import time
import json

from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, \
    StaleElementReferenceException

from selenium_python import smartproxy

# url = 'https://www.walmart.com/ip/Tikland-Wireless-Earbuds-Bluetooth-Earbuds-with-Mic-and-Charging-Case-Deep-Bass-Stereo-IPX7-Waterproof-Mini-Headphones-White/363047257'
url = 'https://www.lowes.com/pd/DEWALT-Jobsite-True-Wireless-Ear-Buds-with-Charging-Case/5002189029'
# url = 'https://www.lowes.com/pd/JVC-Marshmallow-Inner-Ear-Headphones-with-Microphone-Blue/5000110287'

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

options.add_argument(f'user-agent={UserAgent()}')
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')
options.add_argument('--start-fullscreen')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--incognito")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("disable-infobars")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

time_range = 2
# driver.get('https://www.walmart.com/ip/Tikland-Wireless-Earbuds-Bluetooth-Earbuds-with-Mic-and-Charging-Case-Deep-Bass-Stereo-IPX7-Waterproof-Mini-Headphones-White/363047257')

driver.get(url)
time.sleep(3000)




driver.close()
driver.quit()
