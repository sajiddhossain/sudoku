import json
import os

BASE_DIR = os.path.join(os.path.expanduser("~"), ".sudokuforge")
os.makedirs(BASE_DIR, exist_ok=True)
STATS_FILE = os.path.join(BASE_DIR, "stats.json")

if not os.path.exists("data"):
    os.makedirs("data")

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"easy": [], "medium": [], "hard": []}
    try:
        with open(STATS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {"easy": [], "medium": [], "hard": []}
            return json.load(content)
    except (json.JSONDecodeError, ValueError):
        return {"easy": [], "medium": [], "hard": []}
    
def save_stat(difficulty, time_seconds):
    stats = load_stats()
    if difficulty not in stats:
        stats[difficulty] = []
    stats[difficulty].append(time_seconds)
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

def get_best_time(difficulty):
    stats = load_stats()
    times = stats.get(difficulty, [])
    return min(times) if times else None