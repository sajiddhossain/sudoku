import json
import os

FILE_PATH = "data/scores.json"

def get_best_time():
    if not os.path.exists(FILE_PATH):
        return 9999
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
        return data.get("best_time", 9999)
    
def save_best_time(seconds):
    data = {"best_time": seconds}
    os.makedirs("data", exist_ok=True)
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)