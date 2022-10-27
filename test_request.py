import requests
from bs4 import BeautifulSoup
from itertools import cycle
import traceback

import time

url = "https://free-proxy-list.net/"

r = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')

table1 = soup.find('table')

headers = []

for i in table1.find_all('th'):
    title = i.text
    headers.append(title)

print(headers)
proxies = []
for j in table1.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    if row[4] == 'elite proxy':
        proxies.append(f'{row[0]}:{row[1]}')

print(proxies)
proxy_pool = cycle(proxies)
# url = 'https://www.lowes.com/pd/JVC-Marshmallow-Inner-Ear-Headphones-with-Microphone-Blue/5000110287'
url = 'https://httpbin.org/ip'
for i in range(len(proxies)):
    # Get a proxy from the pool
    proxy = next(proxy_pool)
    print("Request #%d" % i)
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        print(response.json())
        print(proxy)
    except Exception:
        # Most free proxies will often get connection errors. You will have retry the entire request using another proxy
        # to work. We will just skip retries as its beyond the scope of this tutorial and we are only downloading a
        # single url
        print("Skipping. Connnection error")

