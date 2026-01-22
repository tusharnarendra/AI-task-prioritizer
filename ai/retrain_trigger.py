import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(__file__)

CSV_PATH = os.path.join(BASE_DIR, "..", "tasks_log.csv")
STATE_PATH = os.path.join(BASE_DIR, "retrain_state.json")

threshold = 20

def retrain_model():
    try:
        df = pd.read_csv(CSV_PATH)
        current = len(df)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    try:
        if os.path.exists(STATE_PATH):
            with open(STATE_PATH, "r") as f:
                state = json.load(f)
            last = state.get("last_count", 0)
        else:
            last = 0
    except Exception as e:
        print(f"Error reading state file: {e}")
        last = 0

    if current - last >= threshold:
        try:
            exit_code = os.system("python3 ai/duration_pred.py")
            if exit_code != 0:
                print(f"Retrain script failed")
        except Exception as e:
            print(f"An unexpected error occurred during execution: {e}")

    try:
        with open(STATE_PATH, "w") as f:
            json.dump({"last_count": current}, f)
    except Exception as e:
        print(f"Error writing state file: {e}")


        
