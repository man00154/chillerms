import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(file):
    path = os.path.join(BASE, "config", file)
    with open(path) as f:
        return json.load(f)

def save_json(file, content):
    path = os.path.join(BASE, "config", file)
    with open(path, "w") as f:
        json.dump(content, f, indent=4)
