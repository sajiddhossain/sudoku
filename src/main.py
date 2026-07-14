import tkinter as tk
from src.gui import draw_grid, button_generate_clicked, resolve_button_clicked, clear_grid, button_hint_clicked, create_note_button, set_timer_label, set_status_label
from src.config import FONT_MAIN
from src.menu import create_start_menu

# main.py

def setup_game_ui(parent_container):
    top_frame = tk.Frame(parent_container)
    top_frame.pack(pady=10)
    timer_label = tk.Label(top_frame, text="00:00", font=FONT_MAIN)
    timer_label.pack()
    set_timer_label(timer_label)

    grid_frame = tk.Frame(parent_container)
    grid_frame.pack(pady=10)
    draw_grid(grid_frame)

    ctrl_frame = tk.Frame(parent_container)
    ctrl_frame.pack(pady=10)

    diff_frame = tk.Frame(ctrl_frame)
    diff_frame.pack()
    tk.Button(diff_frame, text="Easy", command=lambda: button_generate_clicked("easy")).pack(side=tk.LEFT)
    tk.Button(diff_frame, text="Medium", command=lambda: button_generate_clicked("medium")).pack(side=tk.LEFT)
    tk.Button(diff_frame, text="Hard", command=lambda: button_generate_clicked("hard")).pack(side=tk.LEFT)

    action_frame = tk.Frame(ctrl_frame)
    action_frame.pack(pady=10)
    tk.Button(action_frame, text="Solve", command=resolve_button_clicked).pack(side=tk.LEFT)
    tk.Button(action_frame, text="Clear", command=clear_grid).pack(side=tk.LEFT)
    tk.Button(action_frame, text="Hint", command=button_hint_clicked).pack(side=tk.LEFT)
    btn_note = create_note_button(action_frame)
    btn_note.pack(side=tk.LEFT, padx=5)

    status_label = tk.Label(parent_container, text="Ready", font=("Arial", 10), fg="gray")
    status_label.pack(side=tk.BOTTOM, pady=5)
    set_status_label(status_label)

def main():
    root = tk.Tk()
    root.title("Sudoku Forge")
    root.geometry("500x600")

    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    def on_game_start(difficulty):
        for widget in container.winfo_children():
            widget.destroy()
        setup_game_ui(container)
        button_generate_clicked(difficulty)

    create_start_menu(container, on_game_start)

    root.mainloop()

if __name__ == "__main__":
    main()