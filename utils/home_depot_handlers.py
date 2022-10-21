import time
import random

from selenium.webdriver.common.by import By

from utils.Selenium_browser_handler import webdriver_init


def get_hd_shipment_status(url, zip):
    ret_name = 'homedepot.com'
    prod_name = url
    location = zip

    driver = webdriver_init()
    # Starting point
    driver.get('https://www.google.com')
    time.sleep(random.randint(0, 3))
    driver.get(url)

    time.sleep(random.randint(1, 4))
    try:
        # Ship to home Button
        shippint_status = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]'
                                                        '/div/div/div[1]/div/div[2]/a[2]/div/div[2]').text
        if shippint_status == 'Not available for this item':
            return 'Home shipping not available for this item'
        driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div['
                                      '1]/div/div[2]/a[2]').click()
    except Exception:
        return 'Only home delivery (too large of an item) for this item!'

    time.sleep(random.randint(2, 5))
    # clicking on the delivery change button
    driver.find_element(By.XPATH,
                        '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div[1]/div/div[1]/span/span['
                        '2]/button').click()

    # Inputting the zip code
    time.sleep(random.randint(3, 6))
    driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div[1]/div/div['
                                  '2]/div/div/div/div/div[2]/form/div[1]/span/input').clear()
    driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div[1]/div/div['
                                  '2]/div/div/div/div/div[2]/form/div[1]/span/input').send_keys(f'{location}')
    # Clicking update address
    time.sleep(random.randint(4, 7))
    driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div[1]/div/div['
                                  '2]/div/div/div/div/div[2]/form/div[2]/button/span').click()
    time.sleep(random.randint(5, 8))
    in_stock = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div['
                                             '1]/div/div[3]/div[1]/div/span[2]').text
    shipping = 'Ship to Home'
    # Returning delivery status
    return ret_name, prod_name, location, in_stock, shipping
