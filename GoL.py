import pygame
import numpy as np

# Initialize the dimensions of the grid
width, height = 1000, 1000
cell_size = 5
cols, rows = width // cell_size, height // cell_size

# Define colors
alive_color = (255, 255, 255)
dead_color = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Initialize the grid with random states
grid = np.random.choice([0, 1], size=(cols, rows))

# Define the radius for the neighborhood
radius = 1

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

def draw_grid(screen, grid):
    for x in range(cols):
        for y in range(rows):
            color = alive_color if grid[x][y] == 1 else dead_color
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size - 1, cell_size - 1))

running = True
while running:
    screen.fill(dead_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_grid(screen, grid)
    pygame.display.flip()
    grid = update_grid(grid, radius)
    clock.tick(10)

pygame.quit()

