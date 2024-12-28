# Main URL for the swift bet website
MAIN_URL = "https://www.swiftbet.com.au/racing"

# Key panels on the main racing pages
RACE_CONTAINER = "css-7bm4ey-RacesListContainer"
RACE_PANEL = "css-de6u1u-TableData-TableData-RacesRow-RacesField-RacesRow-RacesRow"
RACE_CONTAINER_TITLE = (
    "css-1s043f0-HeaderBar-styled-HeaderBar__Label-HeaderBar-styled-HeaderBar-styled"
)

# The class names for finished and upcoming races are slightly different
RACE_LINK_FINISHED = "css-1qvnyri-RaceItem-RaceItem-RaceItem-RaceItem-RaceItem-RacesRow-RacesRow__RaceItem-RacesRow-RacesRow"
RACE_LINK_JUST_FINISHED = "css-7cdsxu-Text-Text-RaceItem-RaceItem__Status-RaceItem"
RACE_LINK_FINISHED_CONTESTED = "css-c9vt4o-RaceItem-RaceItem-RaceItem-RaceItem-RaceItem-RacesRow-RacesRow__RaceItem-RacesRow-RacesRow"

# There are two link objects for race still to run, depending on if the race is fixed or not
RACE_LINK_FIXED = "css-c9vt4o-RaceItem-RaceItem-RaceItem-RaceItem-RaceItem-RacesRow-RacesRow__RaceItem-RacesRow-RacesRow"
RACE_LINK = "css-17t6czl-RaceItem-RaceItem-RaceItem-RaceItem-RacesRow-RacesRow__RaceItem-RacesRow-RacesRow"

# Grouping for link classes
FINISHED_LINK_CLASSES = [
    RACE_LINK_FINISHED,
    RACE_LINK_JUST_FINISHED,
    RACE_LINK_FINISHED_CONTESTED,
]
LINK_CLASSES = [RACE_LINK_FIXED, RACE_LINK] + FINISHED_LINK_CLASSES

# Status classes
RACE_STATUS_FIXED = "css-1nxhxh1-Text-Text-RaceItem-RaceItem__Status-RaceItem-RaceItem"
RACE_STATUS_ABOUT_TO_START = (
    "css-oxuhgm-Text-Text-RaceItem-RaceItem__Status-RaceItem-RaceItem"
)
RACE_STATUS_JUST_STARTED = "css-1ssi1df-Text-Text-RaceItem-RaceItem__Status-RaceItem"
RACE_STATUS = "css-8e5cal-Text-Text-RaceItem-RaceItem__Status-RaceItem"
RACE_STATUS_CONTESTED = "css-1g6shvk-Text-Text-RaceItem-RaceItem__Status-RaceItem"

# Grouping for status classes
STATUS_CLASSES = [
    RACE_STATUS_FIXED,
    RACE_STATUS_ABOUT_TO_START,
    RACE_STATUS_JUST_STARTED,
    RACE_STATUS,
]

# Regex pattern for extracting the time from the status
DATE_PATTERN = r"(?:(\d+)d\s*)?(?:(\d+)h\s*)?(?:(\d+)m)?"

# Key panels for pricing information
INDIVIDUAL_PRICE_CONTAINER = "css-4tjjy0-RaceSelectionsListItem-RaceSelectionsListItem__Wrapper-RaceSelectionsListItem"
HORSE_NAME = "css-1bpf5z2-Text-Text-RaceSelectionDetails-RaceSelectionsDetails__Name-RaceSelectionDetails-RaceSelectionDetails"
HORSE_PRICE = (
    "css-fvda5w-Text-Text-BettingAdd-styled-BettingAdd__Single-BettingAdd-styled"
)
