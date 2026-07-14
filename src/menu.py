import tkinter as tk
from src.config import get_color
# menu.py

def create_start_menu(window, start_callback):
    menu_frame = tk.Frame(window, bg=get_color("bg"))
    menu_frame.pack(fill="both", expand=True)

    tk.Label(menu_frame, text="SUDOKU FORGE", font=("Arial", 24), bg=get_color("bg"), fg=get_color("fg")).pack(pady=50)

    for diff in ["easy", "medium", "hard"]:
        btn = tk.Button(menu_frame, text=diff.upper(), command=lambda d=diff: [menu_frame.destroy(), start_callback(d)], width=20)
        btn.pack(pady=10)
    return menu_frame