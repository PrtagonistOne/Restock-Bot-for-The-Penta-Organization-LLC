import time
from random import randint

from config.init_logging import init_logging
from config.loggers import get_core_logger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, \
    StaleElementReferenceException

from utils.selenium_utils.Selenium_browser_handler import webdriver_init

init_logging()
logger = get_core_logger()


def change_bbb_address(driver, location, url, time_range):
    # changing address
    while True:
        try:
            time.sleep(time_range)
            # selecting change address button
            product_id = url.split('/')[-1][:7]
            change_zip_code = driver.execute_script(
                f"return document.querySelector('#wmHostPdp').shadowRoot.querySelector('#prod3FulfillmentList{product_id} > "
                "div.i-amphtml-fill-content.i-amphtml-replaced-content > div > div > div.lineH12 > div > div.shipFulfill "
                "> div > div > a')")
            time.sleep(time_range)
            # when the ship to home is not available by default
            if change_zip_code is None:
                change_zip_code = driver.execute_script(
                    f"return document.querySelector('#wmHostPdp').shadowRoot.querySelector('#prod3FulfillmentList{product_id} > div.i-amphtml-fill-content.i-amphtml-replaced-content > div > div > div.lineH12 > div > div.bopisFulfill > div > div:nth-child(1) > a')")

            # selecting change address button
            delivery_options_href = change_zip_code.get_attribute('href')
            time.sleep(time_range)
            driver.get(delivery_options_href)
            time.sleep(time_range)
            # clicking on the change zip code button
            driver.execute_script("return document.querySelector('#formSection > div > label').click()")

            time.sleep(time_range)

            elems = driver.find_elements(By.TAG_NAME, 'input')

            for elem in elems:
                if elem.get_attribute('class') == 's12 input bold':
                    time.sleep(0.8)
                    elem.clear()
                    time.sleep(0.8)
                    elem.send_keys(f'{location}')
                    time.sleep(time_range)
                    button_elems = driver.find_elements(By.TAG_NAME, 'button')
                    for ele in button_elems:
                        if ele.get_attribute('class') == 's12 t6 txtSz bold btn csBtn pickItCsBtn':
                            ele.click()
                            break

        except ElementNotInteractableException:
            logger.info('Changing the Address')
        except NoSuchElementException:
            logger.info('Not in Stock for now')
        except StaleElementReferenceException:
            logger.info('Changing the Zip Code')
            time.sleep(time_range)
            driver.execute_script("return document.querySelector('#fulfillmentModal > div > button').click()")
            time.sleep(time_range)
            break

    logger.info('Changed Address successfully!')


def check_bbb_if_available(driver, time_range):
    time.sleep(time_range)
    # Checking Ship to Home Status
    shipping_status = driver.execute_script(
        "return document.querySelector('#wmHostPdp').shadowRoot.querySelector('#fullfillSelector > div > "
        "div:nth-child(3)').textContent")

    status_check = shipping_status.split()

    if 'Unavailable' in status_check:
        return 'Product Unavailable for Home Shipment'
    else:
        return 'Product in STOCK!'


def get_bbb_shipment_status(url, zip):
    ret_name = 'homedepot.com'
    prod_name = url
    location = zip

    driver = webdriver_init()

    time_range = randint(3, 6)
    driver.get('https://www.google.com')

    driver.get(url)
    time.sleep(time_range)

    change_bbb_address(driver=driver, location=location, url=url, time_range=time_range)

    in_stock = check_bbb_if_available(driver, time_range=time_range)
    shipping = 'Ship to Home'

    driver.close()
    driver.quit()

    # Returning delivery status
    return ret_name, prod_name, location, in_stock, shipping
