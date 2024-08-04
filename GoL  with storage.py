import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import hashlib
import pickle

width, height = 100, 100
cell_size = 5
cols, rows = width // cell_size, height // cell_size

alive_color = (1, 1, 1)  
dead_color = (0, 0, 0)   

grid = np.random.choice([0, 1], size=(cols, rows))

radius = 1

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

recognized_patterns = []

def count_neighbors(grid, x, y, radius):
    count = 0
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if i == 0 and j == 0:
                continue
            count += grid[(x + i) % cols, (y + j) % rows]
    return count

def update_grid(grid, radius):
    new_grid = np.copy(grid)
    for x in range(cols):
        for y in range(rows):
            neighbors = count_neighbors(grid, x, y, radius)
            
            if grid[x, y] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[x, y] = 0
            else:
                if neighbors == 3:
                    new_grid[x, y] = 1
    return new_grid

def meets_alive_cell_requirement(subgrid, min_alive_cells):
    return np.sum(subgrid) >= min_alive_cells


##Improve later
pattern_size_3x3 = 3
pattern_size_4x4 = 4
min_alive_cells_3x3 = pattern_size_3x3**2 - 3
min_alive_cells_4x4 = pattern_size_4x4**2 - 4

def recognize_patterns(grid, recognized_patterns):
    new_recognized_patterns = []
    for x in range(cols - pattern_size_3x3 + 1):
        for y in range(rows - pattern_size_3x3 + 1):
            subgrid_3x3 = grid[x:x+pattern_size_3x3, y:y+pattern_size_3x3]
            if meets_alive_cell_requirement(subgrid_3x3, min_alive_cells_3x3):
                subgrid = subgrid_3x3
                pattern_size = pattern_size_3x3

                if x <= cols - pattern_size_4x4 and y <= rows - pattern_size_4x4:
                    subgrid_4x4 = grid[x:x+pattern_size_4x4, y:y+pattern_size_4x4]
                    if meets_alive_cell_requirement(subgrid_4x4, min_alive_cells_4x4):
                        subgrid = subgrid_4x4
                        pattern_size = pattern_size_4x4

                found = False
                for pattern in recognized_patterns:
                    if np.array_equal(subgrid, pattern.shape):
                        pattern.update_position((x, y))
                        found = True
                        break
                if not found:
                    new_pattern = Pattern(np.copy(subgrid), [(x, y)])
                    recognized_patterns.append(new_pattern)
                    new_recognized_patterns.append(new_pattern)
    return new_recognized_patterns

##Improve later

def save_patterns(patterns, filename):
    with open(filename, 'wb') as f:
        pickle.dump(patterns, f)

def update(grid, radius):
    new_grid = update_grid(grid, radius)
    
    random_mask = np.random.rand(cols, rows) < 0.01
    new_grid[random_mask] = 1 - new_grid[random_mask]
    
    recognize_patterns(new_grid, recognized_patterns)
    recognized_patterns.sort(key=lambda pattern: pattern.count, reverse=True)
    
    top_patterns = recognized_patterns[:10]
    for idx, pattern in enumerate(top_patterns):
        print(f"Top {idx+1} - Pattern ID: {pattern.id}, Count: {pattern.count}, Positions: {pattern.position}, Size: {pattern.size}")
    
    save_patterns(recognized_patterns, 'recognized_patterns.pkl')
    
    return new_grid

def update_animation(frameNum, img, grid, radius):
    grid[:] = update(grid, radius)
    img.set_data(grid)
    return img,

fig, ax = plt.subplots()
img = ax.imshow(grid, cmap='gray', interpolation='nearest')
ani = animation.FuncAnimation(fig, update_animation, fargs=(img, grid, radius), frames=10, interval=100, save_count=50)
plt.show()
