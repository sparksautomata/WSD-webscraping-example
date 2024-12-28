import random
import time


NON_FILE_PATH_CHARACTERS = ["\\", "/", ":", "*", "?", '"', "<", ">", "|", " "]


def clean_string_for_filepath(string: str) -> str:
    for char in NON_FILE_PATH_CHARACTERS:
        string = string.replace(char, "_")
    return string


def random_sleep(min_time: int = 1, max_time: int = 3) -> None:
    time.sleep(random.randint(min_time, max_time))
