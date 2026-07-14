# config.py
# themes
THEMES = {
    "dark": {
        "bg": "black",
        "fg": "white",
        "invalid": "red",
        "highlight": "blue",
        "note": "gray",
        "selected": "orange",
        "cross": "#2F2C2C"
    },
    "light": {
        "bg": "white",
        "fg": "black",
        "invalid": "#ff6b6b",
        "highlight": "lightblue",
        "note": "darkgray",
        "selected": "gold",
        "cross": "#e0e0e0"
    }
}

CURRENT_THEME = "dark"

def get_color(key):
    return THEMES[CURRENT_THEME][key]

# fonts
FONT_MAIN = ("Arial", 16)
FONT_NOTE = ("Arial", 8)
FILES_SCORES = "data/scores.json"
DEFAULT_DIFFICULTY = "medium"