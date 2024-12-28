import os
import re
from bs4 import BeautifulSoup
import pandas as pd
from pydantic import BaseModel
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from swift_bet_scraper.app.constants import MAIN_URL, RACE_CONTAINER
from swift_bet_scraper.app.utils import random_sleep


# TODO: move any of these that are needed to constants.py
TARGET_URL = (
    "https://swiftbet.com.au//racing/gallops/moonee-valley/race-3-1963220-1088174"
)
PRICES_CONTAINER = "css-1w3pfuu-List-List-RaceSelectionsList-RaceSelectionsList__RaceSelectionsListItem-RaceSelectionsList"
INDIVIDUAL_PRICE_CONTAINER = "css-4tjjy0-RaceSelectionsListItem-RaceSelectionsListItem__Wrapper-RaceSelectionsListItem"

HORSE_NAME = "css-1bpf5z2-Text-Text-RaceSelectionDetails-RaceSelectionsDetails__Name-RaceSelectionDetails-RaceSelectionDetails"
HORSE_PRICE = (
    "css-fvda5w-Text-Text-BettingAdd-styled-BettingAdd__Single-BettingAdd-styled"
)

NAVIGATION_BAR = "css-1djnmje-ButtonGroup-ButtonGroup-ButtonGroup-RacingDateSelection-RacingDateSelection-RacingDateSelection-RacingDateSelection-RacingHomePage"
RACE_PANEL = "css-1w3pfuu-List-List-RaceSelectionsList-RaceSelectionsList__RaceSelectionsListItem-RaceSelectionsList"


class HorsePriceInfo(BaseModel):
    name: str
    price: float


class SwiftBetRaceLinkScraper:
    def __init__(self) -> None:
        # setup selenium web driver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    def get_race_price_info(
        self,
        starting_url: str = MAIN_URL,
        target_url: str = TARGET_URL,  # TODO: Create something that pics a pics a random linlk
    ) -> list[BeautifulSoup]:
        try:
            self.driver.get(starting_url)

            # Wait for the page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, RACE_CONTAINER))
            )
            random_sleep()  # add a bit of delay to make the interaction seem more human

            tomorrow = True

            if tomorrow:
                # click the tomorrow button
                tomorrow_button = self.driver.find_element(
                    By.XPATH,
                    "//button[@data-fs-title='page:racing-tab:tomorrow-header_bar']",
                )
                tomorrow_button.click()

            # Wait for race panels to me loaded
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, RACE_PANEL))
            )
            random_sleep()  # add a bit of delay to make the interaction seem more human

            # navigate to the race page
            race_panel = self.driver.find_element(
                By.XPATH, f"//a[@href='{target_url}']"
            )
            race_panel.click()

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, PRICES_CONTAINER))
            )

            full_page = self.driver.page_source
            parsed_page = BeautifulSoup(full_page, "html.parser")
            return parsed_page.find_all("div", class_=INDIVIDUAL_PRICE_CONTAINER)
        finally:
            # Close the browser
            self.driver.quit()

    def __extract_horse_name(self, full_name: str) -> str:
        # Define the regex pattern to match the horse name
        pattern = r"\d+\.\s*(.*?)\(\d+\)"
        match = re.match(pattern, full_name)
        if not match:
            raise ValueError(f"Invalid horse name format: {full_name}")
        return match.group(1)

    def format_price_info(
        self, price_info_panel: BeautifulSoup
    ) -> HorsePriceInfo | None:
        horse_name = price_info_panel.find("div", class_=HORSE_NAME)
        if not horse_name:
            # Non-runner: continue
            return
        horse_price = price_info_panel.find("span", class_=HORSE_PRICE)
        if not horse_price:
            raise ValueError("Could not find horse price")
        return HorsePriceInfo(
            name=self.__extract_horse_name(horse_name.get_text(strip=True)),
            price=float(horse_price.get_text(strip=True)),
        )

    def save_pricing_info(self):
        price_panels = self.get_race_price_info()
        race_info_list = [self.format_price_info(pp) for pp in price_panels]
        df_performed_bets = pd.DataFrame(
            [race.model_dump() for race in race_info_list if race is not None]
        )

        # save out the data to csv
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(
            base_dir,
            "../performed_bets/example_csv.csv",
        )  # TODO, use the target url to name the file_path

        df_performed_bets.to_csv(file_path, index=False)


if __name__ == "__main__":
    scraper = SwiftBetRaceLinkScraper()
    scraper.save_pricing_info()
    # price_panels = scraper.get_race_price_info()
    # for panels in price_panels:
    #     price_info = scraper.format_price_info(panels)
    #     if price_info:
    #         print(price_info.model_dump())
