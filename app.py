import streamlit as st
import pandas as pd
import json
import os
from log import log_energy_page  # Import the Log Energy page
from sleep import sleep_page  # Import the Sleep Log page

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


# Load logs into session state on app start
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
    st.header("📊 Your Logged Entries")

    # Display logs in a table
    if st.session_state["data"]:
        df = pd.DataFrame(st.session_state["data"])
        st.dataframe(df)
    else:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")

elif st.session_state["page"] == "Sleep Log":
    sleep_page()
