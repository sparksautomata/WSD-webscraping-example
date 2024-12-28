from datetime import datetime
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
    "https://swiftbet.com.au//racing/gallops/sapphire-coast/race-2-1963848-1088227"
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


class RandomRace(BaseModel):
    url: str
    is_tomorrow: bool


class SwiftBetRaceLinkScraper:
    def __init__(self) -> None:
        # setup selenium web driver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    def get_race_price_info(
        self,
        starting_url: str = MAIN_URL,
        target_url: str = TARGET_URL,  # TODO: Create something that pics a pics a random link
        tomorrow: bool = False,
    ) -> list[BeautifulSoup]:
        try:
            self.driver.get(starting_url)

            # Wait for the page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, RACE_CONTAINER))
            )
            random_sleep(1, 2)  # Add a random sleep to avoid detection

            if tomorrow:
                # click the tomorrow button
                tomorrow_button = self.driver.find_element(
                    By.XPATH,
                    "//button[@data-fs-title='page:racing-tab:tomorrow-header_bar']",
                )
                tomorrow_button.click()
                random_sleep(
                    3, 5
                )  # TODO: for some reason the WebDriverWait will return true, even though the target element has nto been loaded

            # Wait for race panels to be loaded
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        RACE_CONTAINER,
                    )
                )
            )

            # navigate to the race page
            race_panel = self.driver.find_element(
                By.XPATH, f"//a[@href='{target_url}']"
            )
            race_panel.click()
            random_sleep(1, 2)  # Add a random sleep to avoid detection

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, INDIVIDUAL_PRICE_CONTAINER)
                )
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

    def get_random_unfinished_race(self) -> RandomRace:
        # read all csvs from races_data directory that have todays data a the end of the file name
        all_files = os.listdir(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "../races_data")
        )
        todays_date = datetime.now().date()
        today_files = [
            file
            for file in all_files
            if f"collected_{todays_date.strftime('%Y-%m-%d')}" in file
        ]
        full_dataframe = pd.DataFrame()
        for file in today_files:
            file_df = pd.read_csv(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    f"../races_data/{file}",
                )
            )
            full_dataframe = pd.concat([full_dataframe, file_df])
        # filter only by unfinished races
        unfinished_races = full_dataframe[full_dataframe["time"] != "Finished"]
        # pick a single row at random
        random_race = unfinished_races.sample()
        # check if the race is happing tomorrow - if so we need to navigate to the tomorrow page
        random_race_date = datetime.strptime(
            str(random_race["time"].values[0]), "%Y-%m-%d %H:%M:%S"
        )
        tomorrows_date = todays_date + pd.Timedelta(days=1)
        race_is_tomorrow = random_race_date.date() == tomorrows_date
        return RandomRace(
            url=str(random_race["html_link"].values[0]), is_tomorrow=race_is_tomorrow
        )

    def save_pricing_info(self):
        random_race = self.get_random_unfinished_race()
        price_panels = self.get_race_price_info(
            target_url=random_race.url, tomorrow=random_race.is_tomorrow
        )
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
