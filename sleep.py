import streamlit as st
import datetime
import requests
import base64
import json

# GitHub Configuration
GITHUB_REPO = "hawkarabdulhaq/energy"  # Your GitHub repository
SLEEP_FILE_PATH = "database/sleep.json"  # Path to the sleep file in the repo
HEADERS = {
    "Authorization": f"token {st.secrets['github_pat']}",
    "Accept": "application/vnd.github.v3+json",
}


# Helper Functions
def load_sleep_data_from_github():
    """Load sleep data from the GitHub repository."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{SLEEP_FILE_PATH}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            content = response.json().get("content", "")
            return json.loads(base64.b64decode(content).decode("utf-8"))
        elif response.status_code == 404:
            st.warning("No sleep logs found in the GitHub repository. Initializing empty logs.")
            return []
        else:
            st.error(f"Error loading sleep data from GitHub: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error loading sleep data: {e}")
        return []


def save_sleep_data_to_github(sleep_data):
    """Save sleep data to the GitHub repository."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{SLEEP_FILE_PATH}"
        response = requests.get(url, headers=HEADERS)
        sha = response.json().get("sha", None) if response.status_code == 200 else None

        # Prepare payload
        payload = {
            "message": f"Update sleep logs - {len(sleep_data)} entries",
            "content": base64.b64encode(json.dumps(sleep_data).encode("utf-8")).decode("utf-8"),
        }
        if sha:
            payload["sha"] = sha  # Include SHA if the file exists

        # Send the request
        put_response = requests.put(url, headers=HEADERS, json=payload)
        if put_response.status_code in [200, 201]:
            st.success("Sleep logs successfully saved to GitHub!")
        else:
            st.error(f"Error saving sleep logs to GitHub: {put_response.status_code}")
    except Exception as e:
        st.error(f"Error saving sleep logs: {e}")


def save_sleep_log(sleep_entry, sleep_data):
    """Save a single sleep log entry."""
    st.write(f"DEBUG: Adding sleep log: {sleep_entry}")
    sleep_data.append(sleep_entry)
    save_sleep_data_to_github(sleep_data)
    st.write(f"DEBUG: Sleep log list after adding: {sleep_data}")
    return sleep_data


# Sleep Page
def sleep_page():
    st.title("🌙 Sleep Log")

    # Load sleep data into session state if not already loaded
    if "sleep_data" not in st.session_state:
        st.write("DEBUG: Loading sleep data into session state from GitHub...")
        st.session_state["sleep_data"] = load_sleep_data_from_github()

    # Select Sleep Start Time with Buttons
    st.subheader("1️⃣ What time did you go to sleep?")
    sleep_start_times = [f"{hour:02d}:00" for hour in range(18, 24)] + [f"{hour:02d}:00" for hour in range(0, 7)]
    selected_sleep_start = None

    cols = st.columns(len(sleep_start_times) // 2)
    for i, time in enumerate(sleep_start_times):
        if cols[i % len(cols)].button(time, key=f"sleep_start_{time}"):
            st.session_state["selected_sleep_start"] = time

    if "selected_sleep_start" in st.session_state:
        selected_sleep_start = st.session_state["selected_sleep_start"]
        st.write(f"✅ **Selected Sleep Start Time:** {selected_sleep_start}")

    # Select Wake-Up Time with Buttons
    st.subheader("2️⃣ What time did you wake up?")
    wake_up_times = [f"{hour:02d}:00" for hour in range(4, 12)]
    selected_wake_up = None

    cols = st.columns(len(wake_up_times) // 2)
    for i, time in enumerate(wake_up_times):
        if cols[i % len(cols)].button(time, key=f"wake_up_{time}"):
            st.session_state["selected_wake_up"] = time

    if "selected_wake_up" in st.session_state:
        selected_wake_up = st.session_state["selected_wake_up"]
        st.write(f"✅ **Selected Wake-Up Time:** {selected_wake_up}")

    # Calculate Sleep Duration
    if selected_sleep_start and selected_wake_up:
        sleep_start = datetime.datetime.strptime(selected_sleep_start, "%H:%M").time()
        wake_up = datetime.datetime.strptime(selected_wake_up, "%H:%M").time()

        if wake_up > sleep_start:
            sleep_duration = datetime.datetime.combine(datetime.date.today(), wake_up) - datetime.datetime.combine(datetime.date.today(), sleep_start)
        else:
            sleep_duration = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), wake_up) - datetime.datetime.combine(datetime.date.today(), sleep_start)

        # Display Sleep Duration
        hours, remainder = divmod(sleep_duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        st.write(f"🕒 You slept for **{hours} hours and {minutes} minutes**.")

        # Button to Save Sleep Data
        if st.button("Save Sleep Log", key="save_sleep_log"):
            sleep_entry = {
                "Sleep Start": selected_sleep_start,
                "Wake Up": selected_wake_up,
                "Duration (hrs)": round(hours + minutes / 60, 2),
                "Timestamp": str(datetime.datetime.now())
            }
            save_sleep_log(sleep_entry, st.session_state["sleep_data"])
            st.success("✅ Sleep log saved successfully!")

    # Display Saved Sleep Data
    st.subheader("Your Sleep Records")
    if st.session_state["sleep_data"]:
        st.table(st.session_state["sleep_data"])
    else:
        st.info("No sleep logs recorded yet. Start logging your sleep above.")
