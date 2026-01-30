import json
import os
from datetime import datetime

LOG_FILE = "logs/system.log"

def log(event: dict):
    event["timestamp"] = datetime.utcnow().isoformat()
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
