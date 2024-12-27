from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from swift_bet_scraper.app.constants import MAIN_URL, RACE_CONTAINER


TARGET_URL = "https://swiftbet.com.au//racing/greyhounds/geelong/race-9-1963154-1088166"
PRICES_CONTAINER = "css-1w3pfuu-List-List-RaceSelectionsList-RaceSelectionsList__RaceSelectionsListItem-RaceSelectionsList"
INDIVIDUAL_PRICE_CONTAINER = "css-4tjjy0-RaceSelectionsListItem-RaceSelectionsListItem__Wrapper-RaceSelectionsListItem"


class SwiftBetRaceLinkScraper:
    def __init__(self) -> None:
        # setup selenium web driver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    def get_race_price_info(
        self, starting_url: str = MAIN_URL, target_url: str = TARGET_URL
    ) -> list[BeautifulSoup]:
        self.driver.get(starting_url)

        # Wait for the page to load
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, RACE_CONTAINER))
        )

        # navigate to the race page
        race_panel = self.driver.find_element(By.XPATH, f"//a[@href='{target_url}']")
        race_panel.click()

        # Wait for the race page to load
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, PRICES_CONTAINER))
        )

        full_page = self.driver.page_source
        parsed_page = BeautifulSoup(full_page, "html.parser")

        return parsed_page.find_all("div", class_=INDIVIDUAL_PRICE_CONTAINER)


if __name__ == "__main__":
    scraper = SwiftBetRaceLinkScraper()
    scraper.get_race_price_info()
