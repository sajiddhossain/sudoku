# Sudoku-Forge
A custom Sudoku generator and solver built from scratch in Python and Tkinter.

## Status
Completed - Fully functional game featuring dynamic difficulty, note mode, history undo, theme switching and persistent statistics

## Compatibility & Architecture
- **OS:** macOS
- **Architecture:** Apple Silicon (M1/M2/M3/M4)
- **Build Format:** Native Standalone Executable

## Features
- Procedural Sudoku generation (Easy, Medium, Hard)
- Recursive backtracking solver & hints
- Real-time validation & error highlights
- Note mode & Undo (`Ctrl + Z`)
- Dark/Light themes
- JSON high scores (`S` key)

## How to Run & Play
1. Download `SudokuForge-macOS.zip` from [GitHub Releases](https://github.com/sajiddhossain/sudoku/releases/tag/v1.0.0) and extract it.
2. **First-run:** Open Terminal in the extracted folder and clear the macOS quarantine flag:
   ```
   xattr -cr SudokuForge
   ```
3. Controls: Press `G` to generate a new game, `N` for notes mode, and `S` to check high scores!

## AI Disclosure
AI tools were used during development as a coding collaborator for debugging and application packaging
