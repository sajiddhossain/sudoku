import tkinter
from tkinter import messagebox
from src.grid import resolve
from src.solver import generate_complete_grid, remove_cells
from src.utils import is_valid

# gui.py

cells = [[None for _ in range(9)] for _ in range(9)]

def draw_grid(window):
    for block_r in range(3):
        for block_c in range(3):
            frame = tkinter.Frame(window, highlightbackground="black", highlightthickness=2)
            frame.grid(row=block_r, column=block_c, padx=1, pady=1)

            for i in range(3):
                for j in range(3):
                    r = block_r * 3 + i
                    c = block_c * 3 + j

                    # entry widget for each cell
                    entry = tkinter.Entry(frame, width=3, justify="center")
                    entry.grid(row=i, column=j)
                    entry.bind("<KeyRelease>", lambda event, r=r, c=c: validate_cell(event, r, c))
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
            if value.isdigit() and 1 <= int(value) <= 9:
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
                cells[r][c].config(state="disabled")
            else:
                cells[r][c].config(state="normal")

def validate_cell(event, r, c):
    grid = get_current_grid()
    value = grid[r][c]

    if value == 0:
        cells[r][c].config(bg="white")
        return
    
    grid[r][c] = 0

    if is_valid(grid, r, c, value):
        cells[r][c].config(bg="white")
    else:
        cells[r][c].config(bg="red")

def clear_grid():
    for r in range(9):
        for c in range(9):
            cells[r][c].config(state="normal")
            cells[r][c].delete(0, tkinter.END)
            cells[r][c].config(bg="white")