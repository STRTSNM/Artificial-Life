import pickle
import numpy as np
import matplotlib.pyplot as plt

class Pattern:
    def __init__(self, shape, position):
        self.shape = shape
        self.position = position
        self.id = hashlib.md5(str(shape).encode()).hexdigest()
        self.count = 1
    
    def update_position(self, new_position):
        self.position = new_position
        self.count += 1

def load_patterns(filename):
    with open(filename, 'rb') as f:
        patterns = pickle.load(f)
    return patterns

def visualize_patterns(patterns):
    for idx, pattern in enumerate(patterns):
        plt.figure()
        plt.imshow(pattern.shape, cmap='gray')
        plt.title(f"Pattern ID: {pattern.id}, Count: {pattern.count}")
        plt.show()

if __name__ == "__main__":
    patterns = load_patterns('recognized_patterns.pkl')
    visualize_patterns(patterns)
