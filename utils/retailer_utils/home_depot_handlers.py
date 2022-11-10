import time
from random import randint

from config.init_logging import init_logging
from config.loggers import get_core_logger

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

from utils.selenium_utils.Selenium_browser_handler import webdriver_init

init_logging()
logger = get_core_logger()


def change_hd_address(driver, location, time_range):
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


def check_hd_if_available(driver, time_range):
    while True:
        try:
            time.sleep(time_range)
            elems_fullfill = driver.find_elements(By.CLASS_NAME, 'u__center')
        except ElementNotInteractableException:
            logger.info('Checking shipping status..')
        else:
            delivery_status = set()

            for elem in elems_fullfill:
                for el in elem.get_attribute('class').split():
                    delivery_status.add(el)

            if 'delivery-true' in delivery_status:
                return 'Ship to Home - In-Stock'
            else:
                return 'Home delivery not available for this yet or Out of stock'


def get_hd_shipment_status(url, zip):
    ret_name = 'homedepot.com'
    prod_name = url
    location = zip
    time_range = randint(3, 6)

    driver = webdriver_init()
    # Starting point
    time.sleep(time_range)
    # Moving to the product page
    driver.get(url)
    time.sleep(time_range)

    # Changing the zip code
    logger.info(change_hd_address(driver, location, time_range))

    # Checking the stock
    time.sleep(time_range)
    in_stock = check_hd_if_available(driver, time_range=time_range)
    time.sleep(time_range)

    shipping = 'Ship to Home'

    driver.close()
    driver.quit()

    # Returning delivery status
    return ret_name, prod_name, location, in_stock, shipping
