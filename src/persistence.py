import json
import os

BASE_DIR = os.path.join(os.path.expanduser("~"), ".sudokuforge")
os.makedirs(BASE_DIR, exist_ok=True)
FILE_PATH = "data/scores.json"

def get_best_time():
    if not os.path.exists(FILE_PATH):
        return 9999
    try:
        with open(FILE_PATH, "r") as f:
            content = f.read().strip()
            if not content:
                return 9999
            data = json.loads(content)
            return data.get("best_time", 9999)
    except (json.JSONDecodeError, ValueError):
        return 9999
    
def save_best_time(seconds):
    data = {"best_time": seconds}
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)