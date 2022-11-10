from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

from selenium_python import smartproxy


def webdriver_init():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    ua = UserAgent()
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
    return webdriver.Chrome(service=service, options=options, desired_capabilities=smartproxy())
