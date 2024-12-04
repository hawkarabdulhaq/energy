import os
import bcrypt
import json

USER_DATABASE = "database/users/"

def authenticate_user(username, password):
    user_file = os.path.join(USER_DATABASE, f"{username}.json")
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_data = json.load(file)
            hashed_password = user_data.get("password")
            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                return True
    return False

def create_user(username, password):
    user_file = os.path.join(USER_DATABASE, f"{username}.json")
    if os.path.exists(user_file):
        return False
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user_data = {"password": hashed_password, "entries": []}
    with open(user_file, "w") as file:
        json.dump(user_data, file)
    return True
