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
st.set_page_config(page_title="Energy Log App", layout="wide")  # Wide layout for better button placement
st.title("🌟 Energy Log App")

# Initialize session state
if "data" not in st.session_state:
    st.session_state["data"] = []  # Load from local DB on start

if "selected_activity" not in st.session_state:
    st.session_state["selected_activity"] = None

if "selected_block" not in st.session_state:
    st.session_state["selected_block"] = None


# Helper Functions
def load_local_logs():
    """Load logs from local database file."""
    if os.path.exists(LOCAL_DB_FILE):
        with open(LOCAL_DB_FILE, "r") as file:
            return json.load(file)
    return []


def save_local_logs(logs):
    """Save logs to local database file."""
    with open(LOCAL_DB_FILE, "w") as file:
        json.dump(logs, file, indent=4)


def push_logs_to_github(logs):
    """Push logs to GitHub."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    response = requests.get(url, headers=HEADERS)
    sha = None

    if response.status_code == 200:  # File exists, fetch SHA for updating
        sha = response.json()["sha"]

    commit_message = f"Update energy logs - {datetime.datetime.now()}"
    content = base64.b64encode(json.dumps(logs, indent=4).encode("utf-8")).decode("utf-8")
    payload = {"message": commit_message, "content": content}
    if sha:
        payload["sha"] = sha

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


# Log Energy Page
if st.session_state["page"] == "Log Energy":
    st.header("🔋 Log Your Energy Levels")

    # Step 1: Time Block Selection
    st.subheader("1️⃣ Select Time Block")
    time_blocks = ["6–8 AM", "8–10 AM", "10–12 PM", "12–2 PM", "2–4 PM", "4–6 PM", "6–8 PM"]

    # Display buttons for time block selection
    time_block_cols = st.columns(len(time_blocks))
    for i, block in enumerate(time_blocks):
        if time_block_cols[i].button(block):
            st.session_state["selected_block"] = block

    # Show selected time block
    if st.session_state["selected_block"]:
        st.write(f"✅ **Selected Time Block:** {st.session_state['selected_block']}")

    # Step 2: Energy Level Slider
    st.subheader("2️⃣ Rate Your Energy Level")
    energy_level = st.slider("Rate your energy level (1-10)", 1, 10, 5)

    # Step 3: Activity Type Selection with Buttons
    st.subheader("3️⃣ Select Activity Type")
    activity_categories = get_activity_types()  # Fetch activity categories

    for category, activities in activity_categories.items():
        st.markdown(f"**{category}**")
        activity_cols = st.columns(len(activities))
        for i, activity in enumerate(activities):
            if activity_cols[i].button(activity):
                st.session_state["selected_activity"] = activity

    # Show selected activity
    if st.session_state["selected_activity"]:
        st.write(f"✅ **Selected Activity:** {st.session_state['selected_activity']}")

    # Step 4: Additional Details (Optional)
    st.subheader("4️⃣ Additional Details")
    task = st.text_input("Add more details about the activity (optional):")

    # Step 5: Notes (Optional)
    st.subheader("5️⃣ Notes")
    notes = st.text_area("Add any notes or observations (optional):")

    # Save Entry Button
    if st.button("Save Entry"):
        if st.session_state["selected_block"] and st.session_state["selected_activity"]:
            new_entry = {
                "Time Block": st.session_state["selected_block"],
                "Energy Level": energy_level,
                "Activity Type": st.session_state["selected_activity"],
                "Task": task,
                "Notes": notes,
                "Timestamp": str(datetime.datetime.now()),
            }
            st.session_state["data"].append(new_entry)
            save_local_logs(st.session_state["data"])  # Save to local DB
            push_logs_to_github(st.session_state["data"])  # Auto-sync to GitHub
            st.success("🚀 Entry saved and synced to GitHub!")
            # Reset selections
            st.session_state["selected_block"] = None
            st.session_state["selected_activity"] = None
        else:
            st.error("❌ Please select both a time block and an activity before saving.")

# View Logs Page
elif st.session_state["page"] == "View Logs":
    st.header("📊 Your Logged Entries")

    # Display logs in a table
    if st.session_state["data"]:
        df = pd.DataFrame(st.session_state["data"])
        st.dataframe(df)
    else:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
