# utils.py

def  line_check(grid, r, c, number):
    for column_i in range(9):
        if column_i != c:
            if grid[r][column_i] == number:
                return False
    return True

def box_check(grid, r, c, number):
    start_r = (r // 3) * 3
    start_c = (c // 3) * 3

    for i in range(3):
        for j in range(3):
            current_line = start_r + i
            current_column = start_c + j

            if (current_line != r or current_column != c):
                if grid[current_line][current_column] == number:
                    return False
    return True

def column_check(grid, r, c, number):
    for line_i in range(9):
        if line_i != r:
            if grid[line_i][c] == number:
                return False
    return True

def is_valid(grid, r, c, number):
    if not (0 <= r < 9 and 0 <= c <9):
        return False
    if not (1 <= number <= 9):
        return False
    
    return is_safe(grid, r, c, number)

def exists_in_row(grid, r, c, number):
    for current_column in range(9):
        if current_column == c:
            continue
        if grid[r][current_column] == number:
            return True
    return False

def is_grid_valid(grid):
    for r in range(9):
        for c in range(9):
            value = grid[r][c]
            if value != 0:
                if not line_check(grid, r, c, value): return False
                if not column_check(grid, r, c, value): return False
                if not box_check(grid, r, c, value): return False
    return True

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