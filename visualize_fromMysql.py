import mysql.connector
import json
import numpy as np
import matplotlib.pyplot as plt
import hashlib

DB_CONFIG = {
    'user': 'root',
    'password': 'avrs',
    'host': 'localhost',
    'database': 'project'
}

class Pattern:
    def __init__(self, shape, position):
        self.shape = shape
        self.position = position
        self.id = hashlib.md5(str(shape).encode()).hexdigest()
        self.count = 1
    
    def update_position(self, new_position):
        self.position = new_position
        self.count += 1

def fetch_patterns_from_mysql(db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM patterns"
    cursor.execute(query)
    
    rows = cursor.fetchall()
    
    patterns = []
    for row in rows:
        shape = np.array(json.loads(row['pattern_data'])['shape'])
        position = json.loads(row['pattern_data'])['positions']
        pattern = Pattern(shape, position)
        pattern.id = row['id']
        pattern.count = row['count']
        patterns.append(pattern)
    
    cursor.close()
    conn.close()
    
    return patterns

def visualize_patterns(patterns):
    for idx, pattern in enumerate(patterns):
        plt.figure()
        plt.imshow(pattern.shape, cmap='gray')
        plt.title(f"Pattern ID: {pattern.id}, Count: {pattern.count}")
        plt.show()

if __name__ == "__main__":
    patterns = fetch_patterns_from_mysql(DB_CONFIG)
    
    visualize_patterns(patterns)
