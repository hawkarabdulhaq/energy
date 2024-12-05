import streamlit as st
import pandas as pd
import requests
import json
import datetime
import base64
import os
from activity import get_activity_types  # Import activity types from activity.py

# GitHub Configuration
GITHUB_REPO = "hawkarabdulhaq/energy"  # Your GitHub repository
GITHUB_FILE_PATH = "database/energy_logs.json"  # Path to the file in your repo
GITHUB_PAT = st.secrets["github_pat"]  # Access GitHub PAT from secrets.toml
HEADERS = {
    "Authorization": f"token {GITHUB_PAT}",
    "Accept": "application/vnd.github.v3+json",
}

# Local Database Configuration
LOCAL_DB_FILE = "local_logs.json"  # Local database file

# App Title
st.title("Energy Log App")

# Initialize session state
if "data" not in st.session_state:
    st.session_state["data"] = []  # Load from local DB on start

if "selected_activity" not in st.session_state:
    st.session_state["selected_activity"] = None


# Load local database
def load_local_logs():
    if os.path.exists(LOCAL_DB_FILE):
        with open(LOCAL_DB_FILE, "r") as file:
            return json.load(file)
    return []


# Save logs to local database
def save_local_logs(logs):
    with open(LOCAL_DB_FILE, "w") as file:
        json.dump(logs, file, indent=4)


# Push logs to GitHub
def push_logs_to_github(logs):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    response = requests.get(url, headers=HEADERS)
    sha = None

    if response.status_code == 200:  # File exists, fetch SHA for updating
        sha = response.json()["sha"]

    # Create commit message and content
    commit_message = f"Update energy logs - {datetime.datetime.now()}"
    content = base64.b64encode(json.dumps(logs, indent=4).encode("utf-8")).decode("utf-8")
    payload = {
        "message": commit_message,
        "content": content,
    }
    if sha:
        payload["sha"] = sha  # Add SHA for updates

    # Push data to GitHub
    push_response = requests.put(url, headers=HEADERS, data=json.dumps(payload))
    if push_response.status_code in [200, 201]:
        st.success("Logs synced to GitHub successfully!")
    else:
        st.error(f"Error syncing logs to GitHub: {push_response.status_code}")


# Load logs into session state on app start
if not st.session_state["data"]:
    st.session_state["data"] = load_local_logs()


# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Log Energy"):
    st.session_state["page"] = "Log Energy"
if st.sidebar.button("View Logs"):
    st.session_state["page"] = "View Logs"

# Page: Log Energy
if st.session_state["page"] == "Log Energy":
    st.header("Log Your Energy Levels")

    # Time Block Selection as Buttons
    st.subheader("Select Time Block")
    time_blocks = ["6–8 AM", "8–10 AM", "10–12 PM", "12–2 PM", "2–4 PM", "4–6 PM", "6–8 PM"]

    # Create buttons for time blocks
    cols = st.columns(len(time_blocks))
    for i, block in enumerate(time_blocks):
        if cols[i].button(block):
            st.session_state["selected_block"] = block

    # Display the selected time block
    if st.session_state["selected_block"]:
        st.write(f"**Selected Time Block:** {st.session_state['selected_block']}")

    # Energy Level Input
    st.subheader("Energy Level")
    energy_level = st.slider("Rate your energy level (1-10)", 1, 10, 5)

    # Activity Type Input with Buttons
    st.subheader("Select Activity Type")
    activity_categories = get_activity_types()  # Fetch activity categories

    for category, activities in activity_categories.items():
        st.write(f"**{category}**")
        cols = st.columns(len(activities))
        for i, activity in enumerate(activities):
            if cols[i].button(activity):
                st.session_state["selected_activity"] = activity

    # Display the selected activity
    if st.session_state["selected_activity"]:
        st.write(f"**Selected Activity:** {st.session_state['selected_activity']}")

    # Custom Task Input (Optional)
    task = st.text_input("Additional Details for Activity (Optional)")

    # Notes Input
    st.subheader("Notes")
    notes = st.text_area("Additional Notes (optional)")

    # Button to save log
    if st.button("Save Entry"):
        if st.session_state["selected_block"] and st.session_state["selected_activity"]:
            new_entry = {
                "Time Block": st.session_state["selected_block"],
                "Energy Level": energy_level,
                "Activity Type": st.session_state["selected_activity"],
                "Task": task,
                "Notes": notes,
                "Timestamp": str(datetime.datetime.now())
            }
            st.session_state["data"].append(new_entry)
            save_local_logs(st.session_state["data"])  # Save to local DB
            push_logs_to_github(st.session_state["data"])  # Auto-sync to GitHub
            st.success("Entry saved and synced to GitHub!")
            st.session_state["selected_block"] = None  # Reset selected block
            st.session_state["selected_activity"] = None  # Reset selected activity
        else:
            st.error("Please select both a time block and an activity before saving.")

# Page: View Logs
elif st.session_state["page"] == "View Logs":
    st.header("Your Logged Entries")

    # Display logs if available
    if st.session_state["data"]:
        df = pd.DataFrame(st.session_state["data"])
        st.dataframe(df)
    else:
        st.write("No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
