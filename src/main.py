import tkinter as tk
from src.gui import draw_grid, button_generate_clicked, resolve_button_clicked, clear_grid

def main():
    root = tk.Tk()
    root.title("Sudoku Forge")
    draw_grid(root)

    # button generation
    btn_gen = tk.Button(root, text="Generate Puzzle", command=button_generate_clicked)
    btn_gen.grid(row=4, column=0, columnspan=4)

    btn_solve = tk.Button(root, text="Solve Puzzle", command=resolve_button_clicked)
    btn_solve.grid(row=4, column=2, columnspan=4)

    btn_clear = tk.Button(root, text="Clear Grid", command=clear_grid)
    btn_clear.grid(row=4, column=4, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()