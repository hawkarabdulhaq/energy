import streamlit as st
import os
import json
from log import log_energy_page  # Import the Log Energy page
from sleep import sleep_page  # Import the Sleep Log page
from view import view_logs_page  # Import the View Logs page

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


# Initialize session state for navigation and logs
if "data" not in st.session_state:
    st.session_state["data"] = load_local_logs()

if "page" not in st.session_state:
    st.session_state["page"] = "Log Energy"  # Default page


# Sidebar Navigation with Buttons
st.sidebar.title("Navigation")
if st.sidebar.button("Log Energy"):
    st.session_state["page"] = "Log Energy"
if st.sidebar.button("View Logs"):
    st.session_state["page"] = "View Logs"
if st.sidebar.button("Sleep Log"):
    st.session_state["page"] = "Sleep Log"


# Page Routing
if st.session_state["page"] == "Log Energy":
    log_energy_page(st.session_state["data"], save_local_logs)

elif st.session_state["page"] == "View Logs":
    view_logs_page(st.session_state["data"])

elif st.session_state["page"] == "Sleep Log":
    sleep_page()
