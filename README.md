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
