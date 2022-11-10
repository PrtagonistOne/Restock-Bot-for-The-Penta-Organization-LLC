import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium_python import smartproxy

proxy = 'us.smartproxy.com:10000'

url = 'https://www.bedbathandbeyond.com/store/product/apple-airpods-2-with-wireless-charging-case/300343747?keyword=ear-buds'
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
ua = UserAgent()
# Ready this for more info
# https://www.linkedin.com/pulse/preventing-selenium-from-being-detected-soumil-shah/?trk=articles_directory

options.add_argument(f'user-agent={ua.random}')
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
driver = webdriver.Chrome(service=service, options=options, desired_capabilities=smartproxy())
driver.get(url)
time.sleep(3000)
driver.close()
driver.quit()
