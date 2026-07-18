import json
import os

STATS_FILE = "data/stats.json"

if not os.path.exists("data"):
    os.makedirs("data")

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"easy": [], "medium": [], "hard": []}
    with open(STATS_FILE, "r") as f:
        return json.load(f)
    
def save_stat(difficulty, time_seconds):
    stats = load_stats()
    stats[difficulty].append(time_seconds)
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

def get_best_time(difficulty):
    stats = load_stats()
    times = stats.get(difficulty, [])
    return min(times) if times else None