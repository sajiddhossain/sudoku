import random
from src.utils import is_valid
from src.grid import find_empty_cell

# solver.py

def generate_complete_grid(grid):
    cell = find_empty_cell(grid)
    if cell is None:
        return True # grid is complete
    r, c = cell
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(numbers) # shuffle the numbers to ensure randomness

    for number in numbers:
        if is_valid(grid, r, c, number):
            grid[r][c] = number
            if generate_complete_grid(grid):
                return True
            grid[r][c] = 0

    return False

def remove_cells(grid, num_cells_to_remove):
    while num_cells_to_remove > 0:
        r = random.randint(0, 8)
        c = random.randint(0, 8)

        if grid[r][c] != 0:
            grid[r][c] = 0
            num_cells_to_remove -= 1