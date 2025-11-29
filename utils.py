import json

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, content):
    with open(path, "w") as f:
        json.dump(content, f, indent=4)
