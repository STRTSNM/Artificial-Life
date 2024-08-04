import pickle
import numpy as np
import matplotlib.pyplot as plt
import os
import hashlib

#Pattern class from GoL file
class Pattern:
    def __init__(self, shape, position):
        self.shape = shape
        self.position = position
        self.id = hashlib.md5(str(shape).encode()).hexdigest()
        self.size = shape.shape
        self.count = 1
    
    def update_position(self, new_position):
        self.position = new_position
        self.count += 1


def load_patterns(filename):
    with open(filename, 'rb') as f:
        patterns = pickle.load(f)
    return patterns

def save_pattern_images(patterns, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for idx, pattern in enumerate(patterns):
        fig, ax = plt.subplots()
        ax.imshow(pattern.shape, cmap='gray', interpolation='nearest')
        ax.axis('off')
        
        image_path = os.path.join(output_dir, f'pattern_{idx+1}.png')
        plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

def main():
    patterns = load_patterns('recognized_patterns.pkl')
    
    save_pattern_images(patterns, 'patterns_images')

if __name__ == "__main__":
    main()

