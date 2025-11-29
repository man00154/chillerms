import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------
# Load JSON file (for chillers_config.json)
# ----------------------------------------------------
def load_chiller_config():
    path = os.path.join(BASE, "chillers_config.json")
    with open(path, "r") as f:
        return json.load(f)

# ----------------------------------------------------
# Save updated JSON (ON/OFF or Setpoint update)
# ----------------------------------------------------
def save_chiller_config(data):
    path = os.path.join(BASE, "chillers_config.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
