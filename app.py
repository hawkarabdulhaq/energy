import streamlit as st
import pandas as pd
import requests
import json
import datetime
import base64
import os

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


# Fetch logs from GitHub
def fetch_logs_from_github():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        content = json.loads(base64.b64decode(response.json()["content"]).decode("utf-8"))
        return content
    elif response.status_code == 404:
        st.warning("No logs found in the GitHub repository.")
        return []
    else:
        st.error(f"Error fetching logs from GitHub: {response.status_code}")
        return []


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
        st.success("Logs pushed to GitHub successfully!")
    else:
        st.error(f"Error pushing logs to GitHub: {push_response.status_code}")


# Load logs into session state on app start
if not st.session_state["data"]:
    st.session_state["data"] = load_local_logs()

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Log Energy"):
    st.session_state["page"] = "Log Energy"
if st.sidebar.button("View Logs"):
    st.session_state["page"] = "View Logs"
if st.sidebar.button("Push to GitHub"):
    st.session_state["page"] = "Push to GitHub"

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

    # Task Input
    st.subheader("Task")
    task = st.text_input("What task did you do?")

    # Notes Input
    st.subheader("Notes")
    notes = st.text_area("Additional Notes (optional)")

    # Button to save log
    if st.button("Save Entry"):
        if st.session_state["selected_block"]:
            new_entry = {
                "Time Block": st.session_state["selected_block"],
                "Energy Level": energy_level,
                "Task": task,
                "Notes": notes,
                "Timestamp": str(datetime.datetime.now())
            }
            st.session_state["data"].append(new_entry)
            save_local_logs(st.session_state["data"])  # Save to local DB
            st.success("Entry saved!")
            st.session_state["selected_block"] = None  # Reset selected block
        else:
            st.error("Please select a time block before saving.")

# Page: View Logs
elif st.session_state["page"] == "View Logs":
    st.header("Your Logged Entries")

    # Display logs if available
    if st.session_state["data"]:
        df = pd.DataFrame(st.session_state["data"])
        st.dataframe(df)
    else:
        st.write("No entries logged yet. Go to the 'Log Energy' page to add your first entry.")

# Page: Push to GitHub
elif st.session_state["page"] == "Push to GitHub":
    st.header("Push Your Logs to GitHub")

    if st.button("Fetch Existing Logs"):
        existing_logs = fetch_logs_from_github()
        st.session_state["data"] = existing_logs + st.session_state["data"]
        save_local_logs(st.session_state["data"])  # Save merged logs locally
        st.success("Fetched and merged logs from GitHub!")

    if st.button("Push Logs to GitHub"):
        if st.session_state["data"]:
            push_logs_to_github(st.session_state["data"])
        else:
            st.warning("No logs to push!")
