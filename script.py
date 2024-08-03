import json
import mysql.connector
import os
# Database config to setup
db_config = {
    'host': 'localhost',
    'user': 'user',
    'password': 'password',
    'database': 'database'
}

# Directories to setup
log_directory = '/log_dir'
processed_directory = '/log_dir/processed'

def process_log_file(file_path):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Insert into games table
        cursor.execute("""
            INSERT INTO games (map_name, date, spawn_cycle, max_monsters, cohort_size, zeds_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['mapName'],
            data['date'],
            data['spawnCycle'],
            data['maxMonsters'],
            data['cohortSize'],
            data['zedsType']
        ))
        
        game_id = cursor.lastrowid
        
        # Insert into players table
        for player_data in data['stats']:
            cursor.execute("""
                INSERT INTO players (game_id, alias, steam_id, perk, damage_dealt, accuracy, headshot_accuracy,
                                     large_kills, fleshpounds, scrakes, husks, husk_backpacks, husk_normal,
                                     husk_backpacks_rages, larges_frozen, heals_given, heals_received, damage_taken,
                                     shots_fired, shots_hit, headshots)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                game_id,
                player_data['alias'],
                player_data['steamId'],
                player_data['perk'],
                player_data['damageDealt'],
                player_data['accuracy'],
                player_data['headshotAccuracy'],
                player_data['largeKills'],
                player_data['fleshpounds'],
                player_data['scrakes'],
                player_data['husks'],
                player_data['huskBackpacks'],
                player_data['huskNormal'],
                player_data['huskBackpacksRages'],
                player_data['largesFrozen'],
                player_data['healsGiven'],
                player_data['healsReceived'],
                player_data['damageTaken'],
                player_data['shotsFired'],
                player_data['shotsHit'],
                player_data['headshots']
            ))
        
        connection.commit()
        connection.close()
        # Prints are working if executed manually
        print(f"Processed {file_path}")
        
        # Moving processed file
        os.rename(file_path, os.path.join(processed_directory, os.path.basename(file_path)))
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

os.makedirs(processed_directory, exist_ok=True)

for file_name in os.listdir(log_directory):
    if file_name.endswith('.log') and file_name.startswith('kf'):
        file_path = os.path.join(log_directory, file_name)
        process_log_file(file_path)
