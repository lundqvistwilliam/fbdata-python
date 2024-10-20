
TEAM_NAME_MAP = {
    ## PREMIER LEAGUE
    "Manchester Utd": 'Manchester United',
    "Newcastle Utd": 'Newcastle United',
    "Nott'ham Forest": 'Nottingham Forest',
    "Tottenham": 'Tottenham Hotspur',
    "West Ham": 'West Ham United',
    "Wolves": 'Wolverhampton Wanderers',

    ## LA LIGA
    "Valencia": "Valencia CF",
    "Real Madrid": "Real Madrid CF",
    "Barcelona": "FC Barcelona",
    "Valladolid": 'Real Valladolid',
    
    # Bundesliga
    "Eint Frankfurt": 'Eintracht Frankfurt'
}

def normalize_team_name(scraped_name):
    return TEAM_NAME_MAP.get(scraped_name, scraped_name)
