import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import convolve2d
import hashlib
from collections import defaultdict

# Initialize the dimensions of the grid
width, height = 100, 100
cell_size = 5
cols, rows = width // cell_size, height // cell_size

# Define colors
alive_color = (1, 1, 1)  # White in normalized RGB
dead_color = (0, 0, 0)   # Black in normalized RGB

# Initialize the grid with random states
grid = np.random.choice([0, 1], size=(cols, rows))

# Define the radius for the neighborhood
radius = 1

# Class to represent a pattern
class Pattern:
    def __init__(self, shape, position):
        self.shape = shape  # Numpy array representing the pattern shape
        self.position = position  # List of (x, y) positions where the pattern appears
        self.id = hashlib.md5(str(shape).encode()).hexdigest()  # Unique identifier for the pattern
        self.count = 1  # Initialize occurrence count
    
    def update_position(self, new_position):
        self.position = new_position
        self.count += 1

# List to store recognized patterns
recognized_patterns = []

def count_neighbors(grid, x, y, radius):
    count = 0
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if i == 0 and j == 0:
                continue
            count += grid[(x + i) % cols][(y + j) % rows]
    return count

def update_grid(grid, radius):
    new_grid = np.copy(grid)
    for x in range(cols):
        for y in range(rows):
            neighbors = count_neighbors(grid, x, y, radius)
            
            # Apply Conway's rules
            if grid[x][y] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[x][y] = 0
            else:
                if neighbors == 3:
                    new_grid[x][y] = 1
    return new_grid

def recognize_patterns(grid, recognized_patterns):
    new_recognized_patterns = []
    for x in range(cols):
        for y in range(rows):
            subgrid = grid[x:x+3, y:y+3]  # Considering a 3x3 window
            if subgrid.shape == (3, 3):
                pattern_found = False
                for pattern in recognized_patterns:
                    if np.array_equal(subgrid, pattern.shape):
                        pattern_found = True
                        pattern.update_position((x, y))
                        break
                if not pattern_found:
                    new_pattern = Pattern(np.copy(subgrid), [(x, y)])
                    recognized_patterns.append(new_pattern)
                    new_recognized_patterns.append(new_pattern)
    return new_recognized_patterns

def update(grid, radius):
    # Apply Conway's rules to update the grid
    new_grid = update_grid(grid, radius)
    
    # Introduce random perturbations
    random_mask = np.random.rand(cols, rows) < 0.01  # 1% chance of perturbation
    new_grid[random_mask] = 1 - new_grid[random_mask]  # Flip the state of cells
    
    # Recognize patterns on the updated grid
    new_patterns = recognize_patterns(new_grid, recognized_patterns)
    
    # Sort patterns by occurrence count (descending)
    recognized_patterns.sort(key=lambda pattern: pattern.count, reverse=True)
    
    # Print top 10 patterns
    top_patterns = recognized_patterns[:10]
    for idx, pattern in enumerate(top_patterns):
        print(f"Top {idx+1} - Pattern ID: {pattern.id}, Count: {pattern.count}, Positions: {pattern.position}")
    
    return new_grid

# Update the animation function to use the new update function
def update_animation(frameNum, img, grid, radius):
    grid[:] = update(grid, radius)
    
    img.set_data(grid)
    return img,

# Set up the figure and axis
fig, ax = plt.subplots()
img = ax.imshow(grid, cmap='gray', interpolation='nearest')

# Set up the animation
ani = animation.FuncAnimation(fig, update_animation, fargs=(img, grid, radius), frames=10, interval=100, save_count=50)

plt.show()

