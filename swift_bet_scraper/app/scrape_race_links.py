from datetime import datetime, timedelta
import os
import re
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

from swift_bet_scraper.app.constants import (
    FINISHED_LINK_CLASSES,
    LINK_CLASSES,
    MAIN_URL,
    RACE_CONTAINER,
    RACE_PANEL,
    RACE_CONTAINER_TITLE,
    DATE_PATTERN,
    STATUS_CLASSES,
)

from swift_bet_scraper.app.utils import clean_string_for_filepath

import logging

logger = logging.getLogger(__name__)


class RaceInfo(BaseModel):
    course: str
    race_number: int
    time: str | datetime
    html_link: str


class LinkInfo(BaseModel):
    course: str
    race_number: int
    link: str
    finished: bool = False


class SwiftBetRaceLinkScraper:
    def __init__(self) -> None:
        # setup selenium web driver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    def get_race_list_containers(self, url: str = MAIN_URL) -> list[BeautifulSoup]:
        self.driver.get(url)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, RACE_CONTAINER))
        )

        full_page = self.driver.page_source
        parsed_page = BeautifulSoup(full_page, "html.parser")

        return parsed_page.find_all("div", class_=RACE_CONTAINER)

    def __get_link_info(self, race_panel: BeautifulSoup) -> LinkInfo | None:
        for html_class in LINK_CLASSES:
            link_part = race_panel.find("a", class_=html_class)
            if link_part:
                link = str(link_part.get("href")) or ""  # type: ignore
                split_link = link.split("/")
                race_number = int(split_link[-1].split("-")[1])
                return LinkInfo(
                    course=split_link[-2],
                    race_number=race_number,
                    link=link,
                    finished=html_class in FINISHED_LINK_CLASSES,
                )
        return None

    def __get_race_time(self, race_panel: BeautifulSoup) -> datetime | None:
        for html_class in STATUS_CLASSES:
            status = race_panel.find("div", class_=html_class)
            if status:
                return self.__add_time_to_race_to_current_time(
                    status.get_text(strip=True)
                )
        return None

    def __format_race_info(self, race_panel: BeautifulSoup) -> RaceInfo | None:
        link_info = self.__get_link_info(race_panel)
        if not link_info:
            # empty panel
            return None

        if link_info and link_info.finished:
            return RaceInfo(
                course=link_info.course,
                race_number=link_info.race_number,
                time="Finished",
                html_link=link_info.link,
            )

        race_time = self.__get_race_time(race_panel)
        if not race_time:
            # TODO: figure out why this is failing to get some statuses
            logger.info(
                f"No time found for {link_info.course}: {link_info}. Marking as finished."
            )
            return RaceInfo(
                course=link_info.course,
                race_number=link_info.race_number,
                time="Finished",
                html_link=link_info.link,
            )

        return RaceInfo(
            course=link_info.course,
            race_number=link_info.race_number,
            time=race_time,
            html_link=link_info.link,
        )

    def __add_time_to_race_to_current_time(self, time_str: str) -> datetime:
        # Extract hours and minutes from the input string
        match = re.match(DATE_PATTERN, time_str)
        if not match:
            raise ValueError(
                f"Invalid time format. Expected format 'Xd Yh Zm'. Received: {time_str}"
            )
        days, hours, minutes = [int(x) if x is not None else 0 for x in match.groups()]
        current_time = datetime.now()
        time_delta = timedelta(days=days, hours=hours, minutes=minutes)
        new_time = current_time + time_delta
        new_time = new_time.replace(
            microsecond=0
        )  # Clean the data - milliseconds seems to detailed

        return new_time

    def parse_race_info(
        self,
        day_of_data: str,
        day_of_pull: str,
        race_list_container: BeautifulSoup,
    ) -> None:
        race_type = race_list_container.find("span", class_=RACE_CONTAINER_TITLE)
        logger.info(f"Parsing data for '{day_of_data}' of type '{race_type}'.")
        if race_type is None:
            raise ValueError("Could not parse race type from container.")
        race_type = clean_string_for_filepath(race_type.get_text(strip=True))

        all_race_panels = race_list_container.find_all(
            "div",
            class_=RACE_PANEL,
        )

        # use pydantic to easily convert the data to a dict and then to dataframe
        race_info_list = [self.__format_race_info(rp) for rp in all_race_panels]
        df_races_data = pd.DataFrame(
            [race.model_dump() for race in race_info_list if race is not None]
        )

        # save out the data to csv
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(
            base_dir,
            f"../races_data/{race_type}_{day_of_data}_race_data_collected_{day_of_pull}.csv",
        )

        df_races_data.to_csv(file_path, index=False)

    def generate_all_csvs(self) -> None:
        # Get the containers
        day_mapping = dict()
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        today_str = today.strftime("%Y-%m-%d")
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")
        try:
            day_mapping[today_str] = self.get_race_list_containers()
            day_mapping[tomorrow_str] = self.get_race_list_containers(
                f"{MAIN_URL}/all/{tomorrow_str}"
            )
            for day_of_data, containers in day_mapping.items():
                for container in containers:
                    self.parse_race_info(day_of_data, today_str, container)
        finally:
            self.driver.quit()


if __name__ == "__main__":
    scraper = SwiftBetRaceLinkScraper()
    scraper.generate_all_csvs()
