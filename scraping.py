from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=options)

url = 'https://www.olx.co.id/jakarta-selatan_g4000030/mobil-bekas_c198'

driver.get(url)
time.sleep(5)

for i in range(100):
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, "div._38O09 > button").click()
        time.sleep(5)
    except NoSuchElementException:
        break
time.sleep(5)

products = []
soup = BeautifulSoup(driver.page_source, "html.parser")
for item in soup.findAll('div', class_='_2v8Tq'):
    product_name = item.find('div', class_='_2Gr10').get_text()
    price = item.find('span', class_='_1zgtX').get_text()
    year_km = item.find('div', class_='_21gnE').get_text()
    locations = item.find('div', class_='_3VRSm').get_text()
    products.append(
        (product_name, price, year_km, locations)
    )

df = df = pd.DataFrame(products, columns=['Product Name', 'Price', 'Year-km', 'Locations'])
print(df)

df.to_excel('scraping olx.xlsx', index=False)
print('Data save in local disk')
driver.close