from src.utils import is_valid

# grid.py

def find_empty_cell(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return (r, c) # found an empty cell
    return None # no empty cell found

def resolve(grid):
    cell = find_empty_cell(grid)

    if cell is None:
        return True # no empty cell found, puzzle solved
    
    r, c = cell # otherwise find the row and column

    for number in range(1, 10):
        if is_valid(grid, r, c, number):
            grid[r][c] = number

            if resolve(grid):
                return True
            
            grid[r][c] = 0

    return False # no valid number found

def is_safe(grid, r, c, number):
    for c_i in range(9):
        if (c_i != c) and (grid[r][c_i] == number):
            return False
    
    for r_i in range(9):
        if (r_i != r) and (grid[r_i][c] == number):
            return False
    
    box_r_start = (r // 3) * 3
    box_c_start = (c // 3) * 3

    for i in range(3):
        for j in range(3):
            current_row = box_r_start + i
            current_col = box_c_start + j

            if (current_row != r or current_col != c) and (grid[current_row][current_col] == number):
                return False
            
    return True