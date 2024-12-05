import streamlit as st
import json
import os
from log import log_energy_page  # Import the Log Energy page
from sleep import sleep_page  # Import the Sleep Log page
from view import view_logs_page  # Import the View Logs page
from task import task_page  # Import the Task Management page

# Local Database Configuration
ENERGY_FILE = "local_logs.json"  # Energy logs file
TASK_FILE = "database/task.json"  # Task logs file
SLEEP_FILE = "database/sleep.json"  # Sleep logs file

# Helper Functions
def load_json_file(file_path):
    """Load data from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_json_file(data, file_path):
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# Load logs into session state on app start
if "data" not in st.session_state:
    st.session_state["data"] = load_json_file(ENERGY_FILE)

if "tasks" not in st.session_state:
    st.session_state["tasks"] = load_json_file(TASK_FILE)

if "sleep_data" not in st.session_state:
    st.session_state["sleep_data"] = load_json_file(SLEEP_FILE)

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
    log_energy_page(st.session_state["data"], lambda data: save_json_file(data, ENERGY_FILE))

elif st.session_state["page"] == "Log Sleep":
    sleep_page()

elif st.session_state["page"] == "Log Tasks":
    task_page()

elif st.session_state["page"] == "View Your Energy":
    view_logs_page(
        st.session_state["data"],  # Energy logs
        st.session_state["tasks"],  # Task logs
        st.session_state["sleep_data"],  # Sleep logs
    )
