import os
from datetime import datetime

LOG_DIR = "results/logs"
LOG_FILE = os.path.join(LOG_DIR, "simulation.log")

def log(message, level="INFO"):
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [{level}] {message}"

    # Save to file (FIXED)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

    # Print to console
    print(formatted)