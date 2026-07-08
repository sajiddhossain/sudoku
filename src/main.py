def  line_check(grid, line, number_to_insert, current_column):
    for column_i in range(9):
        if column_i != current_column:
            if grid[line][column_i] == number_to_insert:
                return False
    return True

def box_check(grid, r, c, number):
    start_r = (r // 3) * 3
    start_c = (c // 3) * 3

    for i in range(3):
        for j in range(3):
            current_line = start_r + i
            current_column = start_c + j

            if grid[current_line][current_column] == number:
                return False
    return True