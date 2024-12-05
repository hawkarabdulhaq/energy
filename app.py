import streamlit as st
import json
import os
import requests
from log import log_energy_page  # Import the Log Energy page
from sleep import sleep_page  # Import the Sleep Log page
from view import view_logs_page  # Import the View Logs page
from task import task_page  # Import the Task Management page

# GitHub Configuration
GITHUB_REPO = "hawkarabdulhaq/energy"  # Your GitHub repository
GITHUB_FILE_PATH = "database/local_logs.json"  # Path to the file in your repo
GITHUB_PAT = st.secrets["github_pat"]  # Access GitHub PAT from secrets
HEADERS = {
    "Authorization": f"token {GITHUB_PAT}",
    "Accept": "application/vnd.github.v3+json",
}


# Helper Functions
def load_logs_from_github():
    """Load logs from the GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        content = response.json().get("content", "")
        return json.loads(base64.b64decode(content).decode("utf-8"))
    elif response.status_code == 404:
        st.warning("No logs found in the GitHub repository. Initializing empty logs.")
        return []
    else:
        st.error(f"Error loading logs from GitHub: {response.status_code}")
        return []


def save_logs_to_github(logs):
    """Save logs to the GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    response = requests.get(url, headers=HEADERS)
    sha = response.json().get("sha", None) if response.status_code == 200 else None

    # Prepare payload
    commit_message = f"Update logs - {len(logs)} entries"
    payload = {
        "message": commit_message,
        "content": base64.b64encode(json.dumps(logs).encode("utf-8")).decode("utf-8"),
    }
    if sha:
        payload["sha"] = sha  # Include SHA if the file exists

    # Send the request
    put_response = requests.put(url, headers=HEADERS, json=payload)
    if put_response.status_code in [200, 201]:
        st.success("Logs successfully saved to GitHub!")
    else:
        st.error(f"Error saving logs to GitHub: {put_response.status_code}")


# Load logs into session state on app start
if "data" not in st.session_state:
    st.session_state["data"] = load_logs_from_github()

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
    log_energy_page(st.session_state["data"], save_logs_to_github)

elif st.session_state["page"] == "Log Sleep":
    sleep_page()

elif st.session_state["page"] == "Log Tasks":
    task_page()

elif st.session_state["page"] == "View Your Energy":
    view_logs_page(st.session_state["data"])
