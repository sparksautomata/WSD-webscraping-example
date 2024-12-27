# from bs4 import BeautifulSoup
# import requests

# url = "https://www.scrapethissite.com/pages/forms/"

# page = requests.get(url)
# soup = BeautifulSoup(page.content, "html.parser")

# # div_class = soup.find_all("div", class_="col-md-4")
# print(soup.find_all("div", class_="col-md-12 text-center text-muted"))
# # print(div_class)

# import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from swift_bet_scraper.app.constants import RACE_CONTAINER

# # create webdriver object
# driver = webdriver.Chrome()
# get google.co.in
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    # Open Google
    driver.get("https://www.swiftbet.com.au/racing")

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, RACE_CONTAINER))
    )
finally:
    # Close the browser
    driver.quit()
