from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def webdriver_init():
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)
