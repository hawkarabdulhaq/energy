import streamlit as st
import pandas as pd
import requests
import json
import datetime

# GitHub Configuration
GITHUB_REPO = "hawkarabdulhaq/energy"  # Your GitHub repository
GITHUB_FILE_PATH = "database/energy_logs.json"  # Path to the file in your repo
GITHUB_PAT = st.secrets["github_pat"]  # Access GitHub PAT from secrets.toml
HEADERS = {
    "Authorization": f"token {GITHUB_PAT}",
    "Accept": "application/vnd.github.v3+json",
}

# App Title
st.title("Energy Log App")

# Initialize session state
if "data" not in st.session_state:
    st.session_state["data"] = []

if "page" not in st.session_state:
    st.session_state["page"] = "Log Energy"

if "selected_block" not in st.session_state:
    st.session_state["selected_block"] = None

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Log Energy"):
    st.session_state["page"] = "Log Energy"
if st.sidebar.button("View Logs"):
    st.session_state["page"] = "View Logs"
if st.sidebar.button("Push to GitHub"):
    st.session_state["page"] = "Push to GitHub"

# Function to fetch logs from GitHub
def fetch_logs_from_github():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        content = json.loads(
            requests.get(response.json()["download_url"]).text
        )  # Decode file content
        return content
    elif response.status_code == 404:
        st.warning("No logs found in the GitHub repository.")
        return []
    else:
        st.error("Error fetching logs from GitHub.")
        return []

# Function to push logs to GitHub
def push_logs_to_github(logs):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    response = requests.get(url, headers=HEADERS)
    sha = None

    if response.status_code == 200:  # File exists, fetch SHA for updating
        sha = response.json()["sha"]

    # Create commit message and content
    commit_message = f"Update energy logs - {datetime.datetime.now()}"
    content = json.dumps(logs, indent=4).encode("utf-8").decode("utf-8")
    payload = {
        "message": commit_message,
        "content": content.encode("utf-8").decode("base64"),  # Base64 encoding
    }
    if sha:
        payload["sha"] = sha  # Add SHA for updates

    # Push data to GitHub
    push_response = requests.put(url, headers=HEADERS, data=json.dumps(payload))
    if push_response.status_code in [200, 201]:
        st.success("Logs pushed to GitHub successfully!")
    else:
        st.error("Error pushing logs to GitHub.")

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
            st.session_state["data"].append({
                "Time Block": st.session_state["selected_block"],
                "Energy Level": energy_level,
                "Task": task,
                "Notes": notes,
                "Timestamp": str(datetime.datetime.now())
            })
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
        st.success("Fetched and merged logs from GitHub!")

    if st.button("Push Logs to GitHub"):
        if st.session_state["data"]:
            push_logs_to_github(st.session_state["data"])
        else:
            st.warning("No logs to push!")
