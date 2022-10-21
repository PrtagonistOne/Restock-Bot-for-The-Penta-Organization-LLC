import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager



url = 'https://www.homedepot.com/p/ISOtunes-PRO-Bluetooth-Hearing-Protection-Earbuds-27-dB-Noise-Reduction-Rating' \
      '-OSHA-Compliant-Ear-Protection-for-Work-Orange-IT-01/301358859 '
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://www.google.com')
time.sleep(random.randint(0, 3))
driver.get(url)

time.sleep(random.randint(1, 4))
try:
    # Ship to home Button
    shippint_status = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]'
                                                     '/div/div/div[1]/div/div[2]/a[2]/div/div[2]').text
    if shippint_status == 'Not available for this item':
        print('Home shipping not available for this item')
    driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div['
                                  '1]/div/div[2]/a[2]').click()
except Exception:
    print('Only home delivery (not shipping) for this item!')

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
                              '2]/div/div/div/div/div[2]/form/div[1]/span/input').send_keys('19713')
# Clicking update address
time.sleep(random.randint(4, 7))
driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div[1]/div/div['
                              '2]/div/div/div/div/div[2]/form/div[2]/button/span').click()

# Returning delivery status
time.sleep(random.randint(5, 8))
print(driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/div/div[3]/div/div/div[10]/div/div/div['
                                    '1]/div/div[3]/div[1]/div/span[2]').text)
time.sleep(random.randint(60, 600))

