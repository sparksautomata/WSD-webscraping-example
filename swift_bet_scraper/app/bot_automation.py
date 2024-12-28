from datetime import datetime
import os
import re
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from pandas_to_pydantic import dataframe_to_pydantic

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from swift_bet_scraper.app.constants import (
    HORSE_NAME,
    HORSE_PRICE,
    INDIVIDUAL_PRICE_CONTAINER,
    MAIN_URL,
    RACE_CONTAINER,
)
from swift_bet_scraper.app.utils import clean_string_for_filepath, random_sleep
from swift_bet_scraper.app.scraper_types import HorsePriceInfo, RaceInfo

import logging

logger = logging.getLogger(__name__)


class SwiftBetRaceLinkScraper:
    def __init__(self) -> None:
        # setup selenium web driver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    def get_race_price_info(
        self,
        race_info: RaceInfo,
        starting_url: str = MAIN_URL,
    ) -> list[BeautifulSoup]:
        """
        Get the information for a given race. This includes the horse name and price.
        """
        try:
            self.driver.get(starting_url)

            # Wait for the page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, RACE_CONTAINER))
            )
            random_sleep(1, 2)  # Add a random sleep to avoid detection

            if self.__is_race_tomorrow(race_info.time):
                # click the tomorrow button
                tomorrow_button = self.driver.find_element(
                    By.XPATH,
                    "//button[@data-fs-title='page:racing-tab:tomorrow-header_bar']",
                )
                tomorrow_button.click()
                random_sleep(
                    3, 5
                )  # TODO: for some reason the WebDriverWait will return true, when the element hadn't loaded yet

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
            # TODO: I sometimes get a stale element reference error here - need to investigate
            race_panel = self.driver.find_element(
                By.XPATH, f"//a[@href='{race_info.html_link}']"
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
        """
        Strip out the unnecessary characters in the horse name.
        """
        # Define the regex pattern to match the horse name
        pattern = r"\d+\.\s*(.*?)\(\d+\)"
        match = re.match(pattern, full_name)
        if not match:
            raise ValueError(f"Invalid horse name format: {full_name}")
        return match.group(1)

    def format_price_info(
        self, price_info_panel: BeautifulSoup
    ) -> HorsePriceInfo | None:
        """
        Format the extracted price information.
        """
        horse_name = price_info_panel.find("div", class_=HORSE_NAME)
        if not horse_name:
            # Non-runner: continue
            return
        horse_price = price_info_panel.find("span", class_=HORSE_PRICE)
        if not horse_price:
            raise ValueError("Could not find horse price")
        try:
            price = float(horse_price.get_text(strip=True))
        except ValueError:
            price = horse_price.get_text(
                strip=True
            )  # for when the price is "SP" or similar
        return HorsePriceInfo(
            name=self.__extract_horse_name(horse_name.get_text(strip=True)),
            price=price,
        )

    def get_random_unfinished_race(self) -> RaceInfo:
        """
        Get a random race from all races in race_data that are not finished.
        """
        # read all csvs from races_data directory that have todays data a the end of the file name
        all_files = os.listdir(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "../races_data")
        )
        today_files = [
            file
            for file in all_files
            if f"collected_{datetime.now().strftime('%Y-%m-%d')}" in file
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
        return dataframe_to_pydantic(random_race, RaceInfo).root[0]

    def __is_race_tomorrow(self, date: datetime | str) -> bool:
        if isinstance(date, str):  # pragma: no cover
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        tomorrow = datetime.now() + pd.Timedelta(days=1)
        return date.date() == tomorrow.date()

    def save_pricing_info(self):
        """
        Save out the information to a csv file.
        """
        random_race_info = self.get_random_unfinished_race()
        logger.info(
            f"Getting pricing information for {random_race_info.course}, "
            f"race {random_race_info.race_number} at {random_race_info.time}"
        )
        price_panels = self.get_race_price_info(race_info=random_race_info)
        race_info_list = [self.format_price_info(pp) for pp in price_panels]
        df_performed_bets = pd.DataFrame(
            [race.model_dump() for race in race_info_list if race is not None]
        )

        # save out the data to csv
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if isinstance(random_race_info.time, datetime):
            file_path_time_string = random_race_info.time.strftime("%Y-%m-%d_%H-%M-%S")  # type: ignore
        else:
            file_path_time_string = clean_string_for_filepath(random_race_info.time)
        file_path = os.path.join(
            base_dir,
            f"../performed_bets/prices_{random_race_info.course}_race_{random_race_info.race_number}_{file_path_time_string}.csv",
        )

        df_performed_bets.to_csv(file_path, index=False)


if __name__ == "__main__":
    scraper = SwiftBetRaceLinkScraper()
    scraper.save_pricing_info()
