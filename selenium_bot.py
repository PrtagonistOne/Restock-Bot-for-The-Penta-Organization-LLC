import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementNotInteractableException

url = 'https://www.homedepot.com/p/Google-Nest-Wifi-Mesh-Router-AC2200-and-1-Point-with-Google-Assistant-2-Pack-Snow-GA00822-US/311324762?MERCH=REC-_-sp-_-pip_sponsored-_-1-_-n/a-_-HDProdPage-_-n/a-_-n/a-_-n/a&ITC=AUC-133090-23-12030'

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

time_range = 2
driver.get('https://www.google.com')
time.sleep(random.randint(0, 3))
driver.get(url)


def change_address(driver, location, time_range):
    while True:
        try:
            driver.find_element(By.CLASS_NAME, 'DeliveryZipInline__button').click()
            time.sleep(time_range)
            # Inputting new address and updating it
            driver.find_element(By.ID, 'deliveryZipInput').send_keys(f'{location}')
            time.sleep(time_range)
            driver.find_element(By.ID, 'deliveryZipUpdateButton').click()
            time.sleep(time_range)
        except ElementNotInteractableException:
            print('Changing the Address')
        else:
            return 'Changed Address successfully!'


print(change_address(driver, '03051', 2))

while True:
    try:
        time.sleep(1.5)
        elems_fullfill = driver.find_elements(By.CLASS_NAME, 'u__center')

    except ElementNotInteractableException:
        print('Checking shipping status..')
    else:
        delivery_status = set()

        for elem in elems_fullfill:
            for el in elem.get_attribute('class').split():
                delivery_status.add(el)

        if 'delivery-true' in delivery_status:
            print(delivery_status, 'IT IS IN TTHE DAMN THING!!')
        else:
            print('Home delivery not available for this yet or Out of stock')
            break
