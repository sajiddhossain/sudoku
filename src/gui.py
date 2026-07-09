import tkinter
from tkinter import messagebox
from src.grid import resolve
from src.solver import generate_complete_grid, remove_cells, get_hint
from src.utils import is_valid, is_grid_valid

# gui.py

cells = [[None for _ in range(9)] for _ in range(9)]
DEFAULT_BG = "black"
DEFAULT_FG = "white"
data_grid = [[0 for _ in range(9)] for _ in range(9)]

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
                    entry = tkinter.Entry(frame, width=3, justify="center", bg=DEFAULT_BG, fg=DEFAULT_FG, insertbackground=DEFAULT_FG)
                    entry.grid(row=i, column=j)
                    entry.bind("<KeyRelease>", lambda event, r=r, c=c: validate_cell(event, r, c))
                    cells[r][c] = entry

def create_empty_grid():
    return [[0 for _ in range(9)] for _ in range(9)]

def show_error_message(message):
    messagebox.showerror("Error", message)

def button_generate_clicked():
    new_grid = create_empty_grid()
    generate_complete_grid(new_grid)
    remove_cells(new_grid, 40) # remove 40 cells for the puzzle
    
    for r in range(9):
        for c in range(9):
            data_grid[r][c] = new_grid[r][c]

    update_ui(new_grid)

def resolve_button_clicked():
    count = sum(1 for r in range(9) for c in range(9) if data_grid[r][c] != 0)

    if count < 17:
        show_error_message("Insert at least 17 numbers to resolve a valid puzzle.")
        return

    if not is_grid_valid(data_grid):
        show_error_message("Grid contains conflicts.")
        return
    
    if resolve(data_grid):
        update_ui(data_grid)
    else:
        show_error_message("No solution found.")

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
    value_str = cells[r][c].get()
    value = int(value_str) if value_str.isdigit() and 1 <= int(value_str) <= 9 else 0
    data_grid[r][c] = value
    cells[r][c].config(bg=DEFAULT_BG, fg=DEFAULT_FG)

    if value == 0:
        return

    temp_grid = [row[:] for row in data_grid]
    temp_grid[r][c] = 0

    if not is_valid(temp_grid, r, c, value):
        cells[r][c].config(bg="red", fg="white")

def clear_grid():
    for r in range(9):
        for c in range(9):
            data_grid[r][c] = 0
            cells[r][c].config(state="normal", bg=DEFAULT_BG, fg=DEFAULT_FG)
            cells[r][c].delete(0, tkinter.END)

def button_hint_clicked():
    r, c, value = get_hint(data_grid)
    if value is not None:
        data_grid[r][c] = value
        cells[r][c].delete(0, tkinter.END)
        cells[r][c].insert(0, str(value))
        cells[r][c].config(fg="blue", bg=DEFAULT_BG)
    else:
        show_error_message("No hints available or puzzle is already solved.")