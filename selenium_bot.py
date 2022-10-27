import random
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, \
    StaleElementReferenceException


proxy = '169.57.1.85:8123'

url = 'https://www.lowes.com/pd/Apple-Apple-Ear-Pods-w-3-5mm-Apt/5001893351'
# url = 'https://www.lowes.com/pd/DEWALT-Jobsite-True-Wireless-Ear-Buds-with-Charging-Case/5002189029'
# url = 'https://www.lowes.com/pd/JVC-Marshmallow-Inner-Ear-Headphones-with-Microphone-Blue/5000110287'

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f'--proxy-server={proxy}')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

time_range = 2
driver.get('https://www.google.com')

driver.get(url)
time.sleep(3000)

flag = False
span_text = set()


# def change_address(driver, location, time_range):
while True:
    try:
        time.sleep(3)
        driver.refresh()
        time.sleep(5)
        driver.refresh()

        elems = driver.find_elements(By.TAG_NAME, 'div')

        # Checking delivery availability
        for elem in elems:
            if elem.get_attribute('class') == 'sc-8yiyp5-0 bpvbOY pdp-delivery-zipcode':
                spans = elem.find_elements(By.TAG_NAME, 'span')
                flag = True
                for span in spans:
                    span_text.add(span)
                break

        if 'Delivery to' in span_text or 'Free Delivery to' in span_text:
            print('The item is in stock')
            break

    except ElementNotInteractableException:
        print('Changing the Address')
    except NoSuchElementException:
        print('Not in Stock for now')
    except Exception:
        continue
    else:
        print('Item not in stock')
        break

driver.close()
driver.quit()
