from src.grid import is_safe
# utils.py

def is_valid(grid, r, c, number):
    if not (0 <= r < 9 and 0 <= c <9):
        return False
    if not (1 <= number <= 9):
        return False
    
    return is_safe(grid, r, c, number)

def is_grid_valid(grid):
    for r in range(9):
        for c in range(9):
            value = grid[r][c]
            if value != 0:
                grid[r][c] = 0
                if not is_safe(grid, r, c, value):
                    grid[r][c] = value
                    return False
                grid[r][c] = value
    return True