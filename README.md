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

## How to Play
1. Download the executable from the [GitHub Releases](https://github.com/sajiddhossain/sudoku/releases/tag/v1.0.0) page and extract it
2. **First-run security note:** Because this app is unsigned, macOS might block it the first time. **Right-click (or Control-click)** on `SudokuForge`, select **Open**, and click **Open** again in the prompt
3. Use `G` to generate a new game, `N` for notes, and `S` for high scores!

### Troubleshooting macOS Security (Error: library load disallowed)
If macOS blocks the app or gives a library load error, open your Terminal in the folder where you extracted the app and run this command to clear the quarantine flag:
```
xattr -cr SudokuForge
```

## AI Disclosure
AI tools were used during development as a coding collaborator for debugging and application packaging
