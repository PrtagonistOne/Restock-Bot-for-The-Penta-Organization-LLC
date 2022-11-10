from selenium import webdriver
from selenium_python import get_driver_settings, smartproxy
from selenium.webdriver.common.by import By
import time

def webdriver_example():
    driver = get_driver_settings()
    if driver['DRIVER'] == 'FIREFOX':
        browser = webdriver.Firefox(executable_path=r'{driver_path}'.format(driver_path=driver['DRIVER_PATH']), proxy=smartproxy())
    elif driver['DRIVER'] == 'CHROME':
        browser = webdriver.Chrome(executable_path=r'{driver_path}'.format(driver_path=driver['DRIVER_PATH']), desired_capabilities=smartproxy())
    browser.get('https://ip.smartproxy.com/')
    # browser.get('https://google.com/')

    body_text = browser.find_element(By.TAG_NAME, 'body').text
    time.sleep(1000)
    print(body_text)

if __name__ == '__main__':
    webdriver_example()