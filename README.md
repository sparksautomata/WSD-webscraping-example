# The Brief:
The exercise involves scraping track information, race details, and race times from a
specified website, storing the data in a DataFrame, and saving it as a CSV file. Additionally,
the challenge includes automating a bot to randomly select races, navigate through them
without using direct URLs, scrape market prices for participating horses, and save the results
in another DataFrame, exporting it as a CSV file.
## Challenge 1 - Data Scraping:
1. Visit https://www.swiftbet.com.au/racing
Scrape the following elements from the page:
- Track names
- Race numbers
- URLs of each race (both Australia and NZ)
- Race time (approximated using the time-to-race-start values from the page)
2. Store the collected data in a DataFrame named "df_races_data" and save it as a
CSV file.
3. Ensure that the code can gather information for races scheduled for today and
tomorrow.
## Challenge 2 - Bot Automation:
1. Select a random track and race number from the previously generated CSV.
2. Start from the main races selection page and navigate through the randomly
selected race (avoid using the URL; find a human-like way by searching for
relevant elements within the page).
3. Scrape current market prices for horses participating in the selected race.
4. Save the obtained data into a DataFrame named "df_performed_bets" and export
it as a CSV file.

# How To Run
1. Install poetry if you don't have it already. you can find instructions [here](https://python-poetry.org/docs/#installation).
2. Run `poetry install`
3. Run challenge 1 using `poetry run python swift_bet_scraper/app/data_scraper.py`
4. Run challenge 2 using ` poetry run python swift_bet_scraper/app/bot_automation.py`

# My Approach
 - I opted to save out the data into separate files based on day and race-type, as I found this easier to handle and more human-readable.
 - I quickly discovered most of the elements are dynamically loaded (e.g by Javascript) so needed to employ Selenium over Requests to get the information out.
 - I presumed that finished races are pretty irrelevant (can't bet on a run-race after all) so I overwrote their date as 'Finished' when saving them out to the separate csvs.
 - There are a number of subtle variation in html object that I have mostly caught, but there seem to be a few that crop up when a race goes through state-changes (e.g when a race starts, finishes and is paid-out). I added logging to capture any future ones.
 - I assumed when getting prices we only care about the price of a horse to win.
 - I did not use the race url directly, but the easiest way to tell Selenium what to click on was to search for the url element. Selenium is still acting like a human navigating the site, just using the url to determine what to look at. Very rarely, this will lead to an error. If you rerun the code it should be fine. I have not been able to identify what makes some clicks not work...
 - I also couldn't quite get the `WebDriverWait` when navigating to the Tomorrow page. It was convinced `RACE_CONTAINER` was loaded when navigating to the Tomorrow page even when it was not. Part of the dynamic loading maybe?

