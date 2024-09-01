import json
import os

STORAGE_FILE = 'url_mapping.json'

def save_mapping(url_mapping):
    with open(STORAGE_FILE, 'w') as f:
        json.dump(url_mapping, f)

def load_mapping():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    return {}
