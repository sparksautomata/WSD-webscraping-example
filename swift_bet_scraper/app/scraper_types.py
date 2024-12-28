from datetime import datetime

from pydantic import BaseModel


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


class HorsePriceInfo(BaseModel):
    name: str
    price: float | str
