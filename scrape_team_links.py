import requests
import random
import json
from bs4 import BeautifulSoup

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

headers = {
    'User-Agent': random.choice(user_agents)
}

# List of team URLs containing player links
# 'https://fbref.com/en/squads/18bb7c10/Arsenal-Stats',  # Example URL

team_urls = []

def scrapePlayerLinks():
    all_player_links = []

    for url in team_urls:
        try:
            # time.sleep(random.uniform(1, 5))
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            
            table = soup.find('table', id='stats_standard_9')
            
            if table:
                # Extract player links from this table
                player_elements = table.select('th[data-stat="player"] a')
                
                for player in player_elements:
                    player_href = player.get('href')
                    if player_href:
                        full_url = 'https://fbref.com' + player_href
                        all_player_links.append(full_url)

        except requests.exceptions.RequestException as e:
            print(f"Error scraping {url}: {e}")
        except Exception as e:
            print(f"Error processing data from {url}: {e}")
    
    return json.dumps(all_player_links, indent=2)

player_links_json = scrapePlayerLinks()

print(player_links_json)
