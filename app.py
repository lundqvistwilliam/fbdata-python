from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}


# Initialize MySQL database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

def test_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        database = cursor.fetchone()
        print(f"Connected to database: {database[0]}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

test_db_connection()

def get_team_id_by_name(conn, team_name):
    cursor = conn.cursor()
    
    query = """
    SELECT id 
    FROM club 
    WHERE club_name = %s OR nickname = %s
    """
    
    cursor.execute(query, (team_name, team_name))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None


@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.json
    current_team_name = 'Liverpool' ## CHANGE THIS,
    current_season = '2024-2025'

    # Extract player data
    full_name = data.get('full_name')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    nationality = data.get('nationality')
    position = data.get('position')
    date_of_birth = data.get('date_of_birth')
    team_history = data.get('team_history', [])

    if team_history:
            last_team = team_history[-1]
            last_team_name = last_team.get('team_name')
            last_season = last_team.get('season')

            # Condition to check if the last team is different from the current team, or the season is outdated
            if last_team_name != current_team_name or last_season != current_season:
                # Add new team entry for the current team and season
                new_team_entry = {
                    'season': current_season,
                    'team_name': current_team_name,
                    'competition': 'Premier League'  
                }
                team_history.append(new_team_entry)

    # Save to MySQL database
    conn = get_db_connection()
    cursor = conn.cursor()

    
    try:
        # Insert into players_info table
        cursor.execute('''
            INSERT INTO players_info (full_name, first_name, last_name, nationality, position, image, date_of_birth)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (full_name, first_name, last_name, nationality, position, "", date_of_birth))
        
        player_id = cursor.lastrowid

        # Insert team history into players_team_history table
        for team in team_history:
            season = team.get('season')
            team_name = team.get('team_name')
            competition = team.get('competition')

            team_id = get_team_id_by_name(conn, team_name)


            cursor.execute('''
                  INSERT INTO player_team_history (player_id, team_name, team_id, season, competition, kit_number)
                  VALUES (%s, %s, %s, %s, %s, %s)
              ''', (player_id, team_name, team_id, season, competition, None))  # Kit number is None (empty)

            conn.commit()

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Player and team history added successfully!"}), 201


if __name__ == '__main__':
    app.run(debug=True)
