MAIN_URL = "https://www.swiftbet.com.au/racing"
RACE_CONTAINER = "css-7bm4ey-RacesListContainer"
RACE_PANEL = "css-de6u1u-TableData-TableData-RacesRow-RacesField-RacesRow-RacesRow"
RACE_CONTAINER_TITLE = (
    "css-1s043f0-HeaderBar-styled-HeaderBar__Label-HeaderBar-styled-HeaderBar-styled"
)

# The class names for finished and upcoming races are slightly different
RACE_LINK_FINISHED = "css-1qvnyri-RaceItem-RaceItem-RaceItem-RaceItem-RaceItem-RacesRow-RacesRow__RaceItem-RacesRow-RacesRow"
# There are two link objects for race still to run, depending on if the race is fixed or not
RACE_LINK_FIXED = "css-c9vt4o-RaceItem-RaceItem-RaceItem-RaceItem-RaceItem-RacesRow-RacesRow__RaceItem-RacesRow-RacesRow"
RACE_LINK = "css-17t6czl-RaceItem-RaceItem-RaceItem-RaceItem-RacesRow-RacesRow__RaceItem-RacesRow-RacesRow"

LINK_CLASSES = [RACE_LINK_FINISHED, RACE_LINK_FIXED, RACE_LINK]


RACE_STATUS_FIXED = "css-1nxhxh1-Text-Text-RaceItem-RaceItem__Status-RaceItem-RaceItem"
RACE_STATUS_ABOUT_TO_START = (
    "css-oxuhgm-Text-Text-RaceItem-RaceItem__Status-RaceItem-RaceItem"
)
RACE_STATUS_JUST_STARTED = "css-1ssi1df-Text-Text-RaceItem-RaceItem__Status-RaceItem"
RACE_STATUS = "css-8e5cal-Text-Text-RaceItem-RaceItem__Status-RaceItem"

STATUS_CLASSES = [
    RACE_STATUS_FIXED,
    RACE_STATUS_ABOUT_TO_START,
    RACE_STATUS_JUST_STARTED,
    RACE_STATUS,
]

# use to extract the time information and pass to make calculating datetime easier:
DATE_PATTERN = r"(?:(\d+)d\s*)?(?:(\d+)h\s*)?(?:(\d+)m)?"

# I was using these. I don't think they are needed anymore TODO: remove if no-longer needed
# MEETING_BANNER_CONTAINER = "css-1h8fvx5-TabsItem-TabsItem-TabsItem-TabsItem-TabsItem-TabsItem-TabsItem-TabsItem"
# MEETING_BANNER = "css-lz7t06-Text-Text-Link-Link-MeetingItem-MeetingItem__MeetingName-MeetingItem"
# RUNNER_INFO_CONTAINER = "css-1w3pfuu-List-List-RaceSelectionsList-RaceSelectionsList__RaceSelectionsListItem-RaceSelectionsList"
