import random
from src.utils import is_valid
from src.grid import find_empty_cell, is_safe, resolve

# solver.py

def generate_complete_grid(grid):
    cell = find_empty_cell(grid)
    if cell is None:
        return True # grid is complete
    r, c = cell
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(numbers) # shuffle the numbers to ensure randomness

    for number in numbers:
        if is_safe(grid, r, c, number):
            grid[r][c] = number 

            if generate_complete_grid(grid):
                return True
            
            grid[r][c] = 0

    return False

def remove_cells(grid, count):
    removed = 0
    attempts = 0
    max_attempts = 400

    while removed < count:
        attempts += 1
        r = random.randint(0, 8)
        c = random.randint(0, 8)

        if grid[r][c] != 0:
            backup = grid[r][c]
            grid[r][c] = 0
            
            test_grid = [row[:] for row in grid]

            if solution_count(test_grid) != 1:
                grid[r][c] = backup
            else:
                removed += 1

def solution_count(grid, count=0):
    cell = find_empty_cell(grid)

    if cell is None:
        return count + 1 # found a solution
    
    r, c = cell
    for number in range(1, 10):
        if is_valid(grid, r, c, number):
            grid[r][c] = number
            count = solution_count(grid, count)
            grid[r][c] = 0
            if count >= 2:
                return count
    return count

def get_hint(grid):
    copy_grid = [row[:] for row in grid]

    if resolve(copy_grid):
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    suggested_value = copy_grid[r][c]
                    return (r, c, suggested_value)
    return None, None, None

def is_grid_empty(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                return False
    return True