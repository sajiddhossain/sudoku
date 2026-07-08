import tkinter
from tkinter import messagebox
from src.grid import resolve
from src.solver import generate_complete_grid, remove_cells

cells = [[None for _ in range(9)] for _ in range(9)]

def draw_grid(window):
    for r in range(9):
        for c in range(9):
            # entry widget for each cell
            entry = tkinter.Entry(window, width=2)
            entry.grid(row=r, column=c)
            cells[r][c] = entry

def create_empty_grid():
    return [[0 for _ in range(9)] for _ in range(9)]

def show_error_message(message):
    messagebox.showerror("Error", message)

def button_generate_clicked():
    grid = create_empty_grid()
    generate_complete_grid(grid)
    remove_cells(grid, 40) # remove 40 cells for the puzzle
    update_ui(grid)

def resolve_button_clicked():
    grid = get_current_grid()
    if resolve(grid):
        update_ui(grid)
    else:
        show_error_message("No solution found.")

def get_current_grid():
    new_grid = [[0 for _ in range(9)] for _ in range(9)]
    for r in range(9):
        for c in range(9):
            value = cells[r][c].get()
            if value.isdigit():
                new_grid[r][c] = int(value)
            else:
                new_grid[r][c] = 0
    return new_grid

def update_ui(grid_data):
    for r in range(9):
        for c in range(9):
            cells[r][c].delete(0, tkinter.END)
            if grid_data[r][c] != 0:
                cells[r][c].insert(0, str(grid_data[r][c]))