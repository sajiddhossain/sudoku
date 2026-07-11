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
        if is_safe(grid, r, c, number):
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
    
    start_r, start_c = (r // 3) * 3, (c // 3) * 3

    for i in range(3):
        for j in range(3):

            if (start_r + i != r or start_c + j != c) and (grid[start_r + i][start_c + j] == number):
                return False
            
    return True

def is_valid(grid, r, c, number):
    if not (0 <= r < 9 and 0 <= c < 9): return False
    if not (1 <= number <= 9): return False
    return is_safe(grid, r, c, number)