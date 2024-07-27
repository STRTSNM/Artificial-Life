import mysql.connector
import pickle
import json
import numpy as np

DB_CONFIG = {
    'user': 'root',
    'password': 'avrs',
    'host': 'localhost',
    'database': 'project'
}

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS patterns (
    id VARCHAR(255) PRIMARY KEY,
    size VARCHAR(50),
    count INT,
    positions TEXT,
    pattern_data JSON
);
"""

def load_patterns_from_pickle(filename):
    with open(filename, 'rb') as f:
        patterns = pickle.load(f)
    return patterns

def serialize_pattern(pattern):
    pattern_data = {
        'shape': pattern.shape.tolist(),  # Convert numpy array to list
        'positions': pattern.position
    }
    return json.dumps(pattern_data)

def save_patterns_to_mysql(patterns, db_config):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute(CREATE_TABLE_SQL)
        
        # Insert patterns into the table
        for pattern in patterns:
            pattern_id = pattern.id
            size = f"{pattern.size[0]}x{pattern.size[1]}"
            count = pattern.count
            positions = str(pattern.position)
            pattern_data = serialize_pattern(pattern)
            
            cursor.execute("""
            INSERT INTO patterns (id, size, count, positions, pattern_data)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                size = VALUES(size),
                count = VALUES(count),
                positions = VALUES(positions),
                pattern_data = VALUES(pattern_data)
            """, (pattern_id, size, count, positions, pattern_data))
        
        # Commit and close
        conn.commit()
        print("Patterns have been saved to the MySQL database.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # Load patterns from the pickle file
    patterns = load_patterns_from_pickle('recognized_patterns.pkl')
    
    # Save patterns to the MySQL database
    save_patterns_to_mysql(patterns, DB_CONFIG)
