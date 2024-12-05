import streamlit as st
import json
import os
import base64
import pandas as pd
import datetime
from log import log_energy_page  # Import the Log Energy page
from sleep import sleep_page  # Import the Sleep Log page

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
if "data" not in st.session_state:
    st.session_state["data"] = load_local_logs()


# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Log Energy"):
    st.session_state["page"] = "Log Energy"
if st.sidebar.button("View Logs"):
    st.session_state["page"] = "View Logs"
if st.sidebar.button("Sleep Log"):
    st.session_state["page"] = "Sleep Log"


# Page Routing
if st.session_state.get("page") == "Log Energy":
    log_energy_page(st.session_state["data"], save_local_logs)

elif st.session_state.get("page") == "View Logs":
    st.header("📊 Your Logged Entries")

    # Display logs in a table
    if st.session_state["data"]:
        df = pd.DataFrame(st.session_state["data"])
        st.dataframe(df)
    else:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")

elif st.session_state.get("page") == "Sleep Log":
    sleep_page()
