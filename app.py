import streamlit as st
import os
import json
import bcrypt

# Directory to store user data
USER_DATABASE = "database/users/"
os.makedirs(USER_DATABASE, exist_ok=True)

# Authentication Functions
def authenticate_user(username, password):
    """Authenticate user by checking their username and hashed password."""
    user_file = os.path.join(USER_DATABASE, f"{username}.json")
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_data = json.load(file)
            hashed_password = user_data.get("password")
            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                return True
    return False

def create_user(username, password):
    """Create a new user with hashed password."""
    user_file = os.path.join(USER_DATABASE, f"{username}.json")
    if os.path.exists(user_file):
        return False
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user_data = {"password": hashed_password, "entries": []}
    with open(user_file, "w") as file:
        json.dump(user_data, file)
    return True

# Data Handling Functions
def load_user_data(username):
    """Load the user's data from their JSON file."""
    user_file = os.path.join(USER_DATABASE, f"{username}.json")
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_data = json.load(file)
            return user_data.get("entries", [])
    return []

def save_user_data(username, data):
    """Save the user's data to their JSON file."""
    user_file = os.path.join(USER_DATABASE, f"{username}.json")
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_data = json.load(file)
        user_data["entries"] = data
        with open(user_file, "w") as file:
            json.dump(user_data, file)

# Streamlit App
st.title("Energy Log App")

# Authentication Section
st.sidebar.title("Sign In or Register")
action = st.sidebar.radio("Action", ["Sign In", "Register"])

if action == "Register":
    username = st.sidebar.text_input("Username", key="register_username")
    password = st.sidebar.text_input("Password", type="password", key="register_password")
    if st.sidebar.button("Register"):
        if create_user(username, password):
            st.sidebar.success("User registered successfully. Please sign in.")
        else:
            st.sidebar.error("Username already exists. Please choose a different one.")
elif action == "Sign In":
    username = st.sidebar.text_input("Username", key="signin_username")
    password = st.sidebar.text_input("Password", type="password", key="signin_password")
    if st.sidebar.button("Sign In"):
        if authenticate_user(username, password):
            st.sidebar.success(f"Welcome, {username}!")
            
            # Main App Functionality
            st.subheader(f"Hello, {username}! Log Your Energy Levels Below.")
            data = load_user_data(username)

            # Log Energy Data
            time_block = st.selectbox("Select Time Block", ["6–8 AM", "8–10 AM", "10–12 PM", "12–2 PM", "2–4 PM", "4–6 PM", "6–8 PM"])
            energy_level = st.slider("Energy Level (1-10)", 1, 10)
            task = st.text_input("What task did you do?")
            notes = st.text_area("Additional Notes (optional)")

            if st.button("Save Entry"):
                data.append({"time_block": time_block, "energy_level": energy_level, "task": task, "notes": notes})
                save_user_data(username, data)
                st.success("Entry saved!")

            # Display Daily Entries
            st.subheader("Your Daily Entries")
            for entry in data:
                st.write(f"**{entry['time_block']}**: Energy {entry['energy_level']}/10 | Task: {entry['task']} | Notes: {entry.get('notes', 'N/A')}")

        else:
            st.sidebar.error("Invalid username or password. Please try again.")
