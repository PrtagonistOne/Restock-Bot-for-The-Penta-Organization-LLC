from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://www.homedepot.com/p/RST-Brands-Deco-Estate-Wicker-20-Piece-Patio-Conversation-Set-with-Sunbrella-Charcoal-Grey-Cushions-OP-PEEC20-CHR-K/301626169'

# //*[@id="zipContainer"]/a/div/p[2]/span/svg

driver.get(url)
