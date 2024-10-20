# Project: Player Data Scraper

This project extracts player information and team history from Transfermarkt and Fbref, and integrates it into a database. Below are the steps to use the tool effectively.

---

## 1. Get Squad List of a Team from Transfermarkt

To extract player links from Transfermarkt, follow these steps:

1. **Navigate to the team's Transfermarkt page** (e.g., [Arsenal FC](https://www.transfermarkt.com/fc-arsenal/startseite/verein/11)).
2. **Open the browser console** and run the following script to extract all player links:

    ```javascript
    // Select all <td> elements with the exact class "hauptlink"
    const links = document.querySelectorAll('td.hauptlink:not(.rechts) a');

    // Iterate through the NodeList and extract the href attribute
    const hrefs = Array.from(links).map(link => link.href);

    // Convert the array of hrefs to JSON format
    const hrefsJson = JSON.stringify(hrefs, null, 2);

    // Log the JSON formatted links
    console.log(hrefsJson);
    ```

3. **Copy the resulting player links** and add them to the `player_urls` list in `get_player_data.py`.

> *Note: You may need to remove some links if necessary.*

---

## 2. Get Corresponding Player Links from Fbref

To gather a player's team history from Fbref:

1. **Find the team page on Fbref** (e.g., [Arsenal Stats](https://fbref.com/en/squads/18bb7c10/Arsenal-Stats)).
2. **Run `scrape_team_links.py`** by first adding the Fbref team URL to `team_urls`. Then, run:

    ```bash
    python scrape_team_links.py
    ```

3. **Add the extracted Fbref player URLs** to the `fbref_urls` list in `get_player_data.py`. Ensure that the order matches the `player_urls` list for corresponding player data.

---

## 3. Update Current Team in `app.py`

1. In the `add_player()` function within `app.py`, update the `current_team_name` variable to reflect the current team being scraped.
2. Ensure the team name exactly matches the name in the database to avoid discrepancies.

---

## 4. Run the Application

To start extracting player data:

1. Run the Flask server:

    ```bash
    python app.py
    ```

2. Then run the player data extraction:

    ```bash
    python get_player_data.py
    ```

---

### Additional Notes:
- Ensure your database is set up and connected before running the scripts.
- Keep the player URLs and Fbref URLs in the correct order for seamless data extraction.
