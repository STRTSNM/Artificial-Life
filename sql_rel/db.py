import mysql.connector
import hashlib
import numpy as np
import pickle

# Database connection configuration
db_config = {
    'user': 'root',
    'password': '12345678',
    'host': 'localhost',
    'database': 'patterns_db'
}

def save_top_patterns_to_db(patterns, db_config):
    # Establish a database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Prepare SQL query to insert pattern data
    insert_query = """
    INSERT INTO top_patterns (pattern_id, count, positions, size, pattern)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    # Collect data for insertion
    data_to_insert = []
    for pattern in patterns:
        positions_str = ', '.join(f'({x}, {y})' for x, y in pattern.position)
        size_str = f'{pattern.size[0]}x{pattern.size[1]}'
        pattern_blob = pickle.dumps(pattern.shape)  # Serialize the numpy array to a binary format
        data_to_insert.append((pattern.id, pattern.count, positions_str, size_str, pattern_blob))
    
    # Insert data into the database
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()
    
    # Close the connection
    cursor.close()
    conn.close()

def load_patterns(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_top_patterns(patterns, top_n=20):
    # Sort patterns by count in descending order and get the top N patterns
    return sorted(patterns, key=lambda p: p.count, reverse=True)[:top_n]

def main():
    # Load patterns from file
    patterns = load_patterns('recognized_patterns.pkl')

    # Get top 20 patterns
    top_patterns = get_top_patterns(patterns, top_n=20)

    # Save top patterns to the database
    save_top_patterns_to_db(top_patterns, db_config)
    print("Saved to mysql")

if __name__ == '__main__':
    main()

