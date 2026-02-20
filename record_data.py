import json
import os

def record(data: dict):
    file = "data/data.json"
    records = []
    
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                content = f.read()
                if content.strip():  # only parse if file is not empty
                    records = json.loads(content)
        except json.JSONDecodeError:
            records = []  # if file is corrupted, start fresh
    
    records.append(data)
    
    with open(file, "w") as f:
        json.dump(records, f, indent=4, default=str)  # default=str handles datetime