import streamlit as st
import requests
import json
import base64  # Ensure base64 is imported

# GitHub Configuration
GITHUB_REPO = "hawkarabdulhaq/energy"  # Your GitHub repository
TASKS_FILE_PATH = "database/task.json"  # Path to the task file in the repo
HEADERS = {
    "Authorization": f"token {st.secrets['github_pat']}",
    "Accept": "application/vnd.github.v3+json",
}

# Helper Functions
def load_tasks_from_github():
    """Load tasks from the GitHub repository."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{TASKS_FILE_PATH}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            content = response.json().get("content", "")
            return json.loads(base64.b64decode(content).decode("utf-8"))
        elif response.status_code == 404:
            st.warning("No tasks found in the GitHub repository. Initializing empty tasks.")
            return []
        else:
            st.error(f"Error loading tasks from GitHub: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error loading tasks: {e}")
        return []


def save_tasks_to_github(tasks):
    """Save tasks to the GitHub repository."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{TASKS_FILE_PATH}"
        response = requests.get(url, headers=HEADERS)
        sha = response.json().get("sha", None) if response.status_code == 200 else None

        # Prepare payload
        payload = {
            "message": f"Update tasks - {len(tasks)} entries",
            "content": base64.b64encode(json.dumps(tasks).encode("utf-8")).decode("utf-8"),
        }
        if sha:
            payload["sha"] = sha  # Include SHA if the file exists

        # Send the request
        put_response = requests.put(url, headers=HEADERS, json=payload)
        if put_response.status_code in [200, 201]:
            st.success("Tasks successfully saved to GitHub!")
        else:
            st.error(f"Error saving tasks to GitHub: {put_response.status_code}")
    except Exception as e:
        st.error(f"Error saving tasks: {e}")


def save_task(task_entry, task_data):
    """Save a single task entry."""
    st.write(f"DEBUG: Adding task: {task_entry}")
    task_data.append(task_entry)
    save_tasks_to_github(task_data)
    st.write(f"DEBUG: Task list after adding: {task_data}")
    return task_data


def clean_invalid_tasks(task_data):
    """Remove tasks with invalid data."""
    return [
        task for task in task_data
        if task.get("Task Type") is not None and task.get("Task Length") is not None
    ]


# Task Management Page
def task_page():
    """Task Management Page."""
    st.title("📝 Task Management")

    # Load tasks into session state if not already loaded
    if "tasks" not in st.session_state:
        st.write("DEBUG: Loading tasks into session state from GitHub...")
        st.session_state["tasks"] = clean_invalid_tasks(load_tasks_from_github())

    # Step 1: Select Task Type
    st.subheader("1️⃣ Select Task Type")
    task_types = ["Data Processing", "Writing", "Analysis", "Meeting", "Coding", "Design"]
    cols = st.columns(len(task_types))
    for i, task_type in enumerate(task_types):
        if cols[i].button(task_type, key=f"task_type_{task_type}"):
            st.session_state["selected_task_type"] = task_type

    if "selected_task_type" in st.session_state:
        selected_task_type = st.session_state["selected_task_type"]
        st.write(f"✅ **Selected Task Type:** {selected_task_type}")
    else:
        st.write("DEBUG: No task type selected yet.")

    # Step 2: Select Task Length
    st.subheader("2️⃣ Select Task Length")
    task_lengths = ["Full Day Task", "Half Day Task", "Few Hours Task", "Less than 1 Hour"]
    cols = st.columns(len(task_lengths))
    for i, task_length in enumerate(task_lengths):
        if cols[i].button(task_length, key=f"task_length_{task_length}"):
            st.session_state["selected_task_length"] = task_length

    if "selected_task_length" in st.session_state:
        selected_task_length = st.session_state["selected_task_length"]
        st.write(f"✅ **Selected Task Length:** {selected_task_length}")
    else:
        st.write("DEBUG: No task length selected yet.")

    # Save Task Button
    if st.button("Save Task", key="save_task"):
        if "tasks" not in st.session_state:
            st.session_state["tasks"] = []

        if st.session_state.get("selected_task_type") and st.session_state.get("selected_task_length"):
            new_task = {
                "Task Type": st.session_state["selected_task_type"],
                "Task Length": st.session_state["selected_task_length"],
            }
            st.write(f"DEBUG: New task to save: {new_task}")
            save_task(new_task, st.session_state["tasks"])  # Save task to GitHub
            st.success("✅ Task saved successfully! Add a new task.")
            # Reset session state for a new task
            st.session_state["selected_task_type"] = None
            st.session_state["selected_task_length"] = None
        else:
            st.error("❌ Please select both a task type and a task length before saving.")
            st.write("DEBUG: Attempted to save a task without valid selections.")

    # Display Saved Tasks
    st.subheader("📋 Saved Tasks")
    if st.session_state["tasks"]:
        for idx, task in enumerate(st.session_state["tasks"], start=1):
            st.write(f"{idx}. **{task['Task Type']}** ({task['Task Length']})")
    else:
        st.info("No tasks saved yet.")
