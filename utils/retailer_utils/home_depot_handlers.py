import time
import random

from config.init_logging import init_logging
from config.loggers import get_core_logger

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

from utils.selenium_utils.Selenium_browser_handler import webdriver_init

init_logging()
logger = get_core_logger()


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
            logger.info('Changing the address..')
        else:
            return 'Changed Address successfully!'


def check_if_available(driver, time_range):
    while True:
        try:
            time.sleep(time_range)
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


def get_hd_shipment_status(url, zip):
    ret_name = 'homedepot.com'
    prod_name = url
    location = zip

    driver = webdriver_init()
    # Starting point
    driver.get('https://www.google.com')
    time.sleep(random.randint(6, 15))

    driver.get(url)
    time.sleep(random.randint(15, 30))



    in_stock = 'In-stock'
    shipping = 'Ship to Home'
    # Returning delivery status

    time_range = 2
    driver.get('https://www.google.com')
    driver.maximize_window()
    time.sleep(random.randint(0, 3))
    driver.get(url)

    logger.info(change_address(driver, location, time_range))



    return ret_name, prod_name, location, in_stock, shipping
