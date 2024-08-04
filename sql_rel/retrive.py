import mysql.connector
import numpy as np
import pickle

db_config = {
    'user': 'root',
    'password': '12345678',
    'host': 'localhost',
    'database': 'patterns_db'
}

def retrieve_patterns(db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT pattern_id, count, positions, size, pattern FROM top_patterns"
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Reconstruct patterns
    patterns = []
    for row in rows:
        pattern_id, count, positions, size, pattern_blob = row
        pattern_array = pickle.loads(pattern_blob)  # Deserialize the numpy array from binary format
        size_tuple = tuple(map(int, size.split('x')))
        positions_list = eval(positions)  # string list of tuples
        pattern_obj = {
            'id': pattern_id,
            'count': count,
            'position': positions_list,
            'size': size_tuple,
            'shape': pattern_array
        }
        patterns.append(pattern_obj)

    return patterns

def save_patterns(patterns, filename):
    with open(filename, 'wb') as f:
        pickle.dump(patterns, f)

def main():

    patterns = retrieve_patterns(db_config)
    

    save_patterns(patterns, 'retrieved.pkl')
    print(f"Saved {len(patterns)} patterns to 'retrieved.pkl'.")

if __name__ == '__main__':
    main()

