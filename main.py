from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers)
zillow_page = response.text
soup = BeautifulSoup(zillow_page, "html.parser")


prices = []
for price in soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine"):
    prices.append(price.get_text().strip('+/mobd 1'))

print(prices)

addresses = []
for address in soup.find_all('address'):
    addresses.append(address.getText().strip())

print(addresses)

property_link = soup.select(".StyledPropertyCardDataWrapper a")

links = [link["href"] for link in property_link]
print(links)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(links)):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLScnRUjyz7FUTgGjFhqrVo-e8RKQm4dEcIC1NiOfHRscEXbbng/viewform?usp=sf_link")
    time.sleep(3)

    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(addresses[n])

    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(prices[n])

    time.sleep(2)

    p_links = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    p_links.send_keys(links[n])

    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()

    time.sleep(2)

driver.quit()





