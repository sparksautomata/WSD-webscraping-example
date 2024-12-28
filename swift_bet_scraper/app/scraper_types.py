from datetime import datetime

from pydantic import BaseModel


class RaceInfo(BaseModel):
    course: str
    race_number: int
    time: str | datetime
    html_link: str
