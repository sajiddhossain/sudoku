import tkinter
from tkinter import messagebox
from src.grid import resolve
from src.solver import generate_complete_grid, remove_cells, get_hint
from src.utils import is_valid, is_grid_valid
import time
from src.persistence import get_best_time, save_best_time
from src.config import get_color, FONT_MAIN
from src.stats import save_stat, get_best_time


# gui.py

cells = [[None for _ in range(9)] for _ in range(9)]
data_grid = [[0 for _ in range(9)] for _ in range(9)]
notes_grid = [[set() for _ in range(9)] for _ in range(9)]
is_note_mode = False
btn_note = None
start_time = None
timer_running = False
timer_label = None
timer_job = None
status_label_ref = None
immutable_grid = [[False for _ in range(9)] for _ in range(9)]
undo_stack = []
current_diff = "medium"

def draw_grid(window):
    window.bind_all("<Key>", global_key_handler)
    window.bind_all("<Control-z>", lambda event: undo_last_move())

    window.focus_set()

    for block_r in range(3):
        for block_c in range(3):
            frame = tkinter.Frame(window, highlightbackground=get_color("bg"), highlightthickness=2)
            frame.grid(row=block_r, column=block_c, padx=1, pady=1)

            frame.bind("<Button-1>", lambda event, r=block_r*3, c=block_c*3: highlight_cells(r, c))

            for i in range(3):
                for j in range(3):
                    r = block_r * 3 + i
                    c = block_c * 3 + j

                    # entry widget for each cell
                    entry = tkinter.Entry(frame, width=3, justify="center", bg=get_color("bg"), fg=get_color("fg"), insertbackground=get_color("fg"))
                    vcmd = (window.register(lambda P: P == "" or (P.isdigit() and len(P) == 1 and int(P) > 0)), "%P")
                    entry.config(validate="key", validatecommand=vcmd)
                    entry.grid(row=i, column=j)
                    entry.bind("<KeyRelease>", lambda event, r=r, c=c: validate_cell(event, r, c))
                    cells[r][c] = entry
    
    instructions = tkinter.Label(window, text="G: Generate | T: Theme | N: Note Mode", font=("Arial", 10))
    instructions.grid(row=4, column=0, columnspan=3, pady=5)

def create_empty_grid():
    return [[0 for _ in range(9)] for _ in range(9)]

def show_error_message(message):
    messagebox.showerror("Error", message)

def button_generate_clicked(difficulty="medium"):
    reset_game()
    global start_time, timer_running, current_diff
    current_diff = difficulty
    levels = {"easy": 25, "medium": 40, "hard": 55}
    count = levels.get(difficulty, 40)
    timer_label.config(text="Generating...")
    timer_label.update()
    new_grid = create_empty_grid()
    generate_complete_grid(new_grid)
    remove_cells(new_grid, count) # dynamic number for the puzzle
    start_time = time.time()
    timer_running = True
    update_timer(timer_label)
    
    for r in range(9):
        for c in range(9):
            val = new_grid[r][c]
            data_grid[r][c] = val

            if val != 0:
                cells[r][c].insert(0, str(val))
                cells[r][c].config(state="disabled")
                immutable_grid[r][c] = True
            else:
                immutable_grid[r][c] = False

    update_status(f"Game generated: {difficulty}")
    update_ui(new_grid)

def resolve_button_clicked():
    global timer_running
    timer_running = False
    count = sum(1 for r in range(9) for c in range(9) if data_grid[r][c] != 0)

    if count < 17:
        show_error_message("Insert at least 17 numbers to resolve a valid puzzle.")
        return

    if not is_grid_valid(data_grid):
        show_error_message("Grid contains conflicts.")
        return
    
    timer_running = False
    
    if resolve(data_grid):
        update_status("Puzzle solved by the system!")
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
    old_value = data_grid[r][c]
    value_str = cells[r][c].get()

    if event and event.keysym == "BackSpace":
        if is_note_mode:
            notes_grid[r][c].clear()
            cells[r][c].delete(0, "end")
            return

    if len(value_str) > 2:
        cells[r][c].delete(0, "end")
        return

    if is_note_mode:
        if value_str.isdigit() and "1" <= value_str <= "9":
            value = int(value_str)
            if value in notes_grid[r][c]:
                notes_grid[r][c].remove(value)
            else:
                notes_grid[r][c].add(value)

        cells[r][c].delete(0, "end")
        if notes_grid[r][c]:
            note_text = "".join(sorted(map(str, notes_grid[r][c])))
            cells[r][c].insert(0, note_text)
            cells[r][c].config(fg="gray")
        return
    value = int(value_str) if value_str.isdigit() and 1 <= int(value_str) <= 9 else 0
    if value != old_value:
        undo_stack.append({'r': r, 'c': c, 'val': old_value})
    notes_grid[r][c].clear()
    data_grid[r][c] = value
    cells[r][c].config(bg=get_color("bg"), fg=get_color("fg"))

    if value == 0:
        return

    if not is_valid(data_grid, r, c, value):
        cells[r][c].config(bg=get_color("invalid"), fg=get_color("fg"))

    if check_victory() == True:
        timer_running = False
        messagebox.showinfo("Congratulations! You won")

def clear_grid():
    for r in range(9):
        for c in range(9):
            data_grid[r][c] = 0
            cells[r][c].config(state="normal", bg=get_color("bg"), fg=get_color("fg"))
            cells[r][c].delete(0, tkinter.END)
    if timer_label:
        timer_label.config(text="00:00")
    
    update_status("Grid Cleared.")

def button_hint_clicked():
    r, c, value = get_hint(data_grid)
    if value is not None:
        data_grid[r][c] = value
        cells[r][c].delete(0, tkinter.END)
        cells[r][c].insert(0, str(value))
        cells[r][c].config(fg="blue", bg=get_color("bg"))
        update_status("Hint gived")
    else:
        update_status("No hints available")
        show_error_message("No hints available or puzzle is already solved.")

def toggle_note(r, c, number):
    if number in notes_grid[r][c]:
        notes_grid[r][c].remove(number)
    else:
        notes_grid[r][c].add(number)

def toggle_note_mode():
    global is_note_mode
    is_note_mode = not is_note_mode
    if btn_note:
        btn_note.config(bg="orange" if is_note_mode else "SystemButtonFace")
        status = "Note Mode Activated" if is_note_mode else "Note Mode Disactivated"
        update_status(status)

def create_note_button(window):
    global btn_note
    btn_note = tkinter.Button(window, text="Note Mode", command=toggle_note_mode)
    return btn_note

def update_timer(label):
    global timer_job
    if timer_running:
        elapsed = int(time.time() - start_time)
        minutes, seconds = divmod(elapsed, 60)
        label.config(text=f"{minutes:02d}:{seconds:02d}")
        label.after(1000, lambda: update_timer(label))
    else:
        if timer_job:
            label.after_cancel(timer_job)

def set_timer_label(label):
    global timer_label
    timer_label = label

def check_victory():
    if all(all(row) for row in data_grid) and is_grid_valid(data_grid):
        global timer_running
        timer_running = False

        elapsed_seconds = int(time.time() - start_time)

        current_difficulty = current_diff

        save_stat(current_difficulty, elapsed_seconds)

        best = get_best_time(current_difficulty)

        for r in range(9):
            for c in range(9):
                cells[r][c].config(state="disabled")

        if best == elapsed_seconds or (best is None):
            messagebox.showinfo("Victory!", f"New record: {elapsed_seconds} seconds!")
            update_status("Congratulations! New Record!")
        else:
            messagebox.showinfo("Victory!", f"Completed in {elapsed_seconds} seconds!\nBest time: {best} seconds")
            update_status("Victory! Game completed")
        
        return True

    for row in data_grid:
        for value in row:
            if value == 0:
                return False
    
    return False

def highlight_cells(r, c):
    clicked_value = data_grid[r][c]
    box_start_r, box_start_c = (r // 3) * 3, (c // 3) * 3

    for r_i in range(9):
        for c_i in range(9):
            val = data_grid[r_i][c_i]
            bg_color = get_color("bg")

            if val != 0 and not is_valid(data_grid, r_i, c_i, val):
                bg_color = get_color("invalid")
            
            elif clicked_value != 0 and val == clicked_value:
                bg_color = get_color("highlight")

            elif (r_i == r or c_i == c or (box_start_r <= r_i < box_start_r + 3 and box_start_c <= c_i < box_start_c + 3)):
                bg_color = get_color("cross")

            cells[r_i][c_i].config(state="normal")    
            cells[r_i][c_i].config(bg=bg_color)
            if immutable_grid[r_i][c_i]:
                cells[r_i][c_i].config(state="disabled")

def reset_game():
    global data_grid, notes_grid, timer_running, start_time, immutable_grid

    data_grid = [[0 for _ in range(9)] for _ in range(9)]
    notes_grid = [[set() for _ in range(9)] for _ in range(9)]

    for r in range(9):
        for c in range(9):
            immutable_grid[r][c] = False

    timer_running = False
    start_time = None
    if timer_label:
        timer_label.config(text="00:00")
    
    for r in range(9):
        for c in range(9):
            cells[r][c].delete(0, "end")
            cells[r][c].config(state="normal", bg=get_color("bg"), fg=get_color("fg"))

def refresh_grid_colors():
    for r in range(9):
        for c in range(9):
            val = data_grid[r][c]
            bg_color = get_color("bg")
            if val != 0 and not is_valid(data_grid, r, c, val):
                bg_color = get_color("invalid")

            cells[r][c].config(bg=bg_color)

def handle_cell_input(event, r, c):
    global is_note_mode
    val = cells[r][c].get()
    refresh_grid_colors()

def set_status_label(label):
    global status_label_ref
    status_label_ref = label

def update_status(msg):
    if status_label_ref:
        status_label_ref.config(text=msg)

def on_window_click(event):
    global cells
    widget = event.widget
    
    if isinstance(widget, tkinter.Frame):
        return

    for r in range(9):
        for c in range(9):
            if cells[r][c] == widget:
                highlight_cells(r, c)
                return
            
def toggle_theme():
    import src.config as config
    config.CURRENT_THEME = "light" if config.CURRENT_THEME == "dark" else "dark"

    for r in range(9):
        for c in range(9):
            cells[r][c].config(bg=config.get_color("bg"), fg=config.get_color("fg"))
            refresh_grid_colors()

def global_key_handler(event):
    key = event.keysym.lower()

    if key in ["t", "n", "g", "s"]:
        if key == "t": toggle_theme()
        elif key == "n": toggle_note_mode()
        elif key == "g": button_generate_clicked()
        elif key == "s": show_stats_window(event.widget.winfo_toplevel())
        return "break"

def record_move(r, c, old_val):
    undo_stack.append({"r": r, "c": c, "val": old_val})

def undo_last_move():
    if not undo_stack:
        update_status("No moves to undo!")
        return
    
    move = undo_stack.pop()
    r, c, old_val = move["r"], move["c"], move["val"]
    data_grid[r][c] = old_val
    cells[r][c].delete(0, "end")
    if old_val != 0:
        cells[r][c].insert(0, str(old_val))
    cells[r][c].config(bg=get_color("bg"), fg=get_color("fg"))
    refresh_grid_colors()
    update_status(f"Undo: restored ({r+1}, {c+1})")
    return "break"

def show_stats_window(parent_window):
    import json
    import os

    stats_file = "data/scores.json"

    stats_win = tkinter.Toplevel(parent_window)
    stats_win.title("Statistics & High scores")
    stats_win.geometry("300x250")
    stats_win.resizable(False, False)
    stats_win.configure(bg=get_color("bg"))

    title_label = tkinter.Label(
        stats_win,
        text="Best times",
        font=("Arial", 16, "bold"),
        bg=get_color("bg"),
        fg=get_color("fg")
    )
    title_label.pack(pady=10)

    scores = {}
    if os.path.exists(stats_file):
        try:
            with open(stats_file, "r") as f:
                scores = json.load(f)
        except Exception:
            scores = {}
    
    difficulties = ["easy", "medium", "hard"]

    frame = tkinter.Frame(stats_win, bg=get_color("bg"))
    frame.pack(pady=10, fill="x", padx=20)

    for diff in difficulties:
        best_time = scores.get(diff, None)
        if best_time is not None:
            time_str = f"{best_time // 60:02d}:{best_time % 60:02d}"
        else:
            time_str = "--:--"
        
        row_frame = tkinter.Frame(frame, bg=get_color("bg"))
        row_frame.pack(fill="x", pady=5)

        lbl_diff = tkinter.Label(
            row_frame,
            text=f"{diff.capitalize()}:",
            font=("Arial", 12, "bold"),
            bg=get_color("bg"),
            fg=get_color("fg"),
            anchor="w"
        )
        lbl_diff.pack(side="left")

        lbl_val = tkinter.Label(
            row_frame,
            text=time_str,
            font=("Arial", 12),
            bg=get_color("bg"),
            fg=get_color("fg"),
            anchor="e"
        )
        lbl_diff.pack(side="right")

        btn_close = tkinter.Button(
            stats_win,
            text="Close",
            command=stats_win.destroy,
            bg=get_color("selected"),
            fg="black"
        )
        btn_close.pack(pady=15)