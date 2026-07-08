import tkinter as tk
from src.gui import draw_grid, button_generate_clicked, resolve_button_clicked

def main():
    root = tk.Tk()
    root.title("Sudoku Forge")
    draw_grid(root)

    # button generation
    btn_gen = tk.Button(root, text="Generate Puzzle", command=button_generate_clicked)
    btn_gen.grid(row=10, column=0, columnspan=4)

    btn_solve = tk.Button(root, text="Solve Puzzle", command=resolve_button_clicked)
    btn_solve.grid(row=10, column=5, columnspan=4)

    root.mainloop()

if __name__ == "__main__":
    main()