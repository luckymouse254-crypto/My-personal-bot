import json, os
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"chat_id": None, "expenses": [], "notes": [], "habits": {}, "water": [], "todos": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"chat_id": None, "expenses": [], "notes": [], "habits": {}, "water": [], "todos": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_chat_id(chat_id):
    data = load_data()
    data["chat_id"] = chat_id
    save_data(data)

def get_chat_id():
    return load_data().get("chat_id")

def log_expense(amount, reason):
    data = load_data()
    data["expenses"].append({"amount": amount, "reason": reason, "time": str(datetime.now())})
    save_data(data)
    return data["expenses"]

def log_note(note):
    data = load_data()
    data["notes"].append({"text": note, "time": str(datetime.now())})
    save_data(data)

def log_water():
    data = load_data()
    data["water"].append(str(datetime.now()))
    save_data(data)
    today = datetime.now().date().isoformat()
    return len([w for w in data["water"] if today in w])

def add_todo(text):
    data = load_data()
    data["todos"].append({"text": text, "done": False, "time": str(datetime.now())})
    save_data(data)
