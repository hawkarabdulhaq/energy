import os
import json

USER_DATABASE = "database/users/"

def load_user_data(username):
    user_file = os.path.join(USER_DATABASE, f"{username}.json")
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_data = json.load(file)
            return user_data.get("entries", [])
    return []

def save_user_data(username, data):
    user_file = os.path.join(USER_DATABASE, f"{username}.json")
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_data = json.load(file)
        user_data["entries"] = data
        with open(user_file, "w") as file:
            json.dump(user_data, file)
