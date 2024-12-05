import streamlit as st
import json
import os
import requests
import base64
from log import log_energy_page   # Import the Log Energy page
from sleep import sleep_page      # Import the Sleep Log page
from view import view_logs_page   # Import the View Logs page
from task import task_page        # Import the Task Management page

# GitHub Configuration
GITHUB_REPO = "hawkarabdulhaq/energy"  # Your GitHub repository
ENERGY_FILE_PATH = "database/local_logs.json"  # Energy logs file in repo
TASK_FILE_PATH = "database/task.json"          # Task logs file in repo
SLEEP_FILE_PATH = "database/sleep.json"        # Sleep logs file in repo
GITHUB_PAT = st.secrets["github_pat"]          # Access GitHub PAT from secrets

HEADERS = {
    "Authorization": f"token {GITHUB_PAT}",
    "Accept": "application/vnd.github.v3+json",
}

# Helper Functions
def load_data_from_github(file_path):
    """Load data from a specified JSON file in the GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        content = response.json().get("content", "")
        if content:
            return json.loads(base64.b64decode(content).decode("utf-8"))
        else:
            # File is empty but exists
            return []
    elif response.status_code == 404:
        st.warning(f"No data found for {file_path} in the GitHub repository. Initializing empty dataset.")
        return []
    else:
        st.error(f"Error loading data from {file_path} on GitHub: {response.status_code}")
        return []

def save_data_to_github(file_path, data):
    """Save data to a specified JSON file in the GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    response = requests.get(url, headers=HEADERS)
    sha = response.json().get("sha", None) if response.status_code == 200 else None

    commit_message = f"Update {os.path.basename(file_path)} - {len(data)} entries"
    payload = {
        "message": commit_message,
        "content": base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8"),
    }
    if sha:
        payload["sha"] = sha

    put_response = requests.put(url, headers=HEADERS, json=payload)
    if put_response.status_code in [200, 201]:
        st.success(f"Data successfully saved to {file_path} on GitHub!")
    else:
        st.error(f"Error saving data to GitHub ({file_path}): {put_response.status_code}")

# Load logs into session state on app start
if "data" not in st.session_state:
    # Energy logs
    st.session_state["data"] = load_data_from_github(ENERGY_FILE_PATH)

if "tasks" not in st.session_state:
    # Task data
    st.session_state["tasks"] = load_data_from_github(TASK_FILE_PATH)

if "sleep_data" not in st.session_state:
    # Sleep data
    st.session_state["sleep_data"] = load_data_from_github(SLEEP_FILE_PATH)

if "page" not in st.session_state:
    st.session_state["page"] = "Log Energy"  # Default page

# Sidebar Navigation with Buttons
st.sidebar.title("Navigation")
if st.sidebar.button("Log Energy"):
    st.session_state["page"] = "Log Energy"
if st.sidebar.button("Log Sleep"):
    st.session_state["page"] = "Log Sleep"
if st.sidebar.button("Log Tasks"):
    st.session_state["page"] = "Log Tasks"
if st.sidebar.button("View Your Energy"):
    st.session_state["page"] = "View Your Energy"

# Page Routing
if st.session_state["page"] == "Log Energy":
    # Save energy logs back to GitHub
    log_energy_page(st.session_state["data"], lambda logs: save_data_to_github(ENERGY_FILE_PATH, logs))

elif st.session_state["page"] == "Log Sleep":
    # Sleep logs handled in sleep.py (If needed, integrate GitHub saving there)
    sleep_page()

elif st.session_state["page"] == "Log Tasks":
    # Tasks handled in task.py (If needed, integrate GitHub saving there)
    task_page()

elif st.session_state["page"] == "View Your Energy":
    # Now passing energy logs, tasks, and sleep data
    view_logs_page(st.session_state["data"], st.session_state["tasks"], st.session_state["sleep_data"])
