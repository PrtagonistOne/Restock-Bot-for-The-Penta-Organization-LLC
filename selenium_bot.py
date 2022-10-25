import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException

# url = 'https://www.bedbathandbeyond.com/store/product/altec-lansing-xbox-surround-sound-over-the-ear-gaming-headset-with-microphone-in-black/5568466?skuId=69680556&strategy=pdp_fbt'
# url = 'https://www.bedbathandbeyond.com/store/product/sharper-image-soundhaven-sport-over-the-ear-true-wireless-earbuds-in-black/5754710?skuId=69930636'
url = 'https://www.bedbathandbeyond.com/store/product/sharper-image-the-sound-of-unity-wireless-earbuds/5577529'
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

time_range = 2
driver.get('https://www.google.com')

driver.get(url)
time.sleep(3)

# def change_address(driver, location, time_range):
while True:
    try:
        time.sleep(3)
        product_id = url.split('/')[-1][:7]
        change_zip_code = driver.execute_script(
            f"return document.querySelector('#wmHostPdp').shadowRoot.querySelector('#prod3FulfillmentList{product_id} > "
            "div.i-amphtml-fill-content.i-amphtml-replaced-content > div > div > div.lineH12 > div > div.shipFulfill "
            "> div > div > a')")
        time.sleep(0.5)
        if change_zip_code is None:
            change_zip_code = driver.execute_script(
                f"return document.querySelector('#wmHostPdp').shadowRoot.querySelector('#prod3FulfillmentList{product_id} > div.i-amphtml-fill-content.i-amphtml-replaced-content > div > div > div.lineH12 > div > div.bopisFulfill > div > div:nth-child(1) > a')")
        delivery_options_href = change_zip_code.get_attribute('href')
        time.sleep(2.6)
        driver.get(delivery_options_href)
        time.sleep(3)

        change_location_button = driver.execute_script("return document.querySelector('#formSection > div > label').click()")
        time.sleep(2.6)

        elems = driver.find_elements(By.TAG_NAME, 'input')

        for elem in elems:
            if elem.get_attribute('class') == 's12 input bold':
                time.sleep(0.8)
                elem.clear()
                time.sleep(0.8)
                elem.send_keys('97217')
                time.sleep(1.8)
                button_elems = driver.find_elements(By.TAG_NAME, 'button')
                for ele in button_elems:
                    if ele.get_attribute('class') == 's12 t6 txtSz bold btn csBtn pickItCsBtn':
                        ele.click()
                        break

    except ElementNotInteractableException:
        print('Changing the Address')
    except NoSuchElementException:
        print('Not in Stock for now')
    except StaleElementReferenceException:
        print('Changing the Zip Code')
        time.sleep(2.5)
        driver.execute_script("return document.querySelector('#fulfillmentModal > div > button').click()")
        time.sleep(2.5)
        break

print('Changed Address successfully!')

time.sleep(3)
# Checking Ship to Home Status
shipping_status = driver.execute_script(
    "return document.querySelector('#wmHostPdp').shadowRoot.querySelector('#fullfillSelector > div > div:nth-child(3)').textContent")

status_check = shipping_status.split()

if 'Unavailable' in status_check:
    print('Product Unavailable for Home Shipment')
else:
    print('Product in STOCK!')
time.sleep(0.5)

driver.close()
driver.quit()
