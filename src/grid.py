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