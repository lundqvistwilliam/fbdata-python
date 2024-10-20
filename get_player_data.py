import re
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
from team_name_map import normalize_team_name


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]
headers = {
    'User-Agent': random.choice(user_agents)
}

# List of player URLs from Transfermarkt
player_urls = [
  
]

# Corresponding fbref URLs in the same order as player_urls
fbref_urls = [
 
]



# Flask API URL
flask_api_url = 'http://127.0.0.1:5000/add_player'

def convertDobToDateFormat(dob):
    month_abbr_to_num = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
        'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
        'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    date_part = dob.split('(')[0].strip()
    try:
        date_obj = datetime.strptime(date_part, '%b %d, %Y')
        month = date_obj.month
        day = date_obj.day
        year = date_obj.year
        sql_date_format = f'{year:04d}-{month:02d}-{day:02d}'
        return sql_date_format
    except ValueError:
        return None

def convertPosition(position):
    if position in ('Centre-Back', 'Left-Back', 'Right-Back'):
        return 'Defender'
    if position in ('Defensive Midfield', 'Central Midfield', 'Attacking Midfield'):
        return 'Midfielder'
    if position in ('Left Winger', 'Right Winger', 'Centre-Forward'):
        return 'Forward'
    return 'Unknown'

def send_data_to_flask(player_info):
    try:
        response = requests.post(flask_api_url, json=player_info)
        response.raise_for_status()
        print(f"Successfully added player: {player_info['full_name']}")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# scrape player team history from fbref
def scrapePlayerTeamHistoryData(fbref_url):
    player_table_data = []
    try:
        time.sleep(random.uniform(1, 5))
        response = requests.get(fbref_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', id='stats_standard_dom_lg')

        if not table:
            print(f"Table not found for {fbref_url}")
            return []

        rows = table.find_all('tr', id="stats")
        print("Scraping team history for: ",fbref_url + "...")


        for row in rows:
            season = row.select_one('th[data-stat="year_id"]').text.strip() if row.select_one('th[data-stat="year_id"]') else "N/A"
            team = row.select_one('td[data-stat="team"] a').text.strip() if row.select_one('td[data-stat="team"] a') else "N/A"
            competition = row.select_one('td[data-stat="comp_level"] a').text.strip() if row.select_one('td[data-stat="comp_level"] a') else "N/A"

            player_table_data.append({
                'season': season,
                'team_name': team,
                'competition': competition,
            })

    except requests.RequestException as e:
        print(f"Error scraping {fbref_url}: {e}")

    return player_table_data

# scrape player data from Transfermarkt
def scrapePlayerData():
    for i, url in enumerate(player_urls):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            player_name = soup.select_one('h1.data-header__headline-wrapper').text.split('\n')[-1].strip()
            print("Scraping player info: ",player_name + "...")

            name_parts = player_name.split(' ', 1)
            if len(name_parts) == 1: ## Players with single name
                first_name = ''
                last_name = name_parts[0]  
            else:
                first_name = name_parts[0]
                last_name = name_parts[1]

            player_position = re.search(r'Position:\s*<span class="data-header__content">\s*(.*?)\s*</span>', str(soup))
            player_position = player_position.group(1) if player_position else 'Unknown'

            dob_li = soup.select_one('li.data-header__label:has(span[itemprop="birthDate"])')
            dob_span = dob_li.select_one('span[itemprop="birthDate"]') if dob_li else None
            player_date_of_birth = dob_span.get_text(strip=True) if dob_span else 'Unknown'

            citizenship_li = soup.select_one('li.data-header__label:has(span[itemprop="nationality"])')
            nationality_alt = citizenship_li.select_one('span[itemprop="nationality"] img').get('alt') if citizenship_li else 'Unknown'

            if player_position != 'Goalkeeper':
                player_position = convertPosition(player_position)

            convertedPlayerDob = convertDobToDateFormat(player_date_of_birth)

            player_info = {
                "full_name": player_name,
                "first_name": first_name,
                "last_name": last_name,
                "nationality": nationality_alt,
                "position": player_position,
                "date_of_birth": convertedPlayerDob,
            }

            # Scrape team history from FBref for the corresponding player
            if i < len(fbref_urls):  # Ensure there's a corresponding FBref URL
                team_history = scrapePlayerTeamHistoryData(fbref_urls[i])
                player_info['team_history'] = team_history

            send_data_to_flask(player_info)

            time.sleep(random.uniform(5, 10))

        except requests.RequestException as e:
            print(f"Request error for {url}: {e}")

scrapePlayerData()