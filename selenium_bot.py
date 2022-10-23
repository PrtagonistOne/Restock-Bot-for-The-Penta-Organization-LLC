import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementNotInteractableException

url = 'https://www.homedepot.com/p/Zenith-Stereo-Earbuds-with-Microphone-in-Blue-PM1001SEB2/305896604'

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

time_range = 2
driver.get('https://www.google.com')
driver.maximize_window()
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
            print('')
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
