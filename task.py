import streamlit as st
import os
import json

# Path to the tasks JSON file
TASKS_JSON_FILE = "database/task.json"

# Helper Functions
def load_tasks():
    """Load tasks from the task.json file."""
    try:
        if os.path.exists(TASKS_JSON_FILE):
            st.write(f"DEBUG: Loading tasks from {TASKS_JSON_FILE}")
            with open(TASKS_JSON_FILE, "r") as file:
                return json.load(file)
        else:
            st.write(f"DEBUG: {TASKS_JSON_FILE} does not exist. Returning an empty list.")
            return []
    except Exception as e:
        st.error(f"Error loading tasks: {e}")
        return []

def save_to_local(tasks):
    """Save tasks to the task.json file with enhanced debugging."""
    try:
        st.write("DEBUG: Saving tasks to file...")
        os.makedirs(os.path.dirname(TASKS_JSON_FILE), exist_ok=True)
        with open(TASKS_JSON_FILE, "w") as file:
            json.dump(tasks, file, indent=4)

        # Check if the file exists and display its contents
        if os.path.exists(TASKS_JSON_FILE):
            st.write(f"DEBUG: {TASKS_JSON_FILE} exists.")
            with open(TASKS_JSON_FILE, "r") as file:
                saved_data = json.load(file)
                st.write(f"DEBUG: Content of {TASKS_JSON_FILE}: {saved_data}")
        else:
            st.error(f"DEBUG: {TASKS_JSON_FILE} was not created.")

        st.write("DEBUG: Tasks saved successfully.")
    except Exception as e:
        st.error(f"Error saving tasks: {e}")


def save_task(task_entry, task_data):
    """Save a single task entry."""
    st.write(f"DEBUG: Adding task: {task_entry}")
    task_data.append(task_entry)
    save_to_local(task_data)
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
        st.write("DEBUG: Loading tasks into session state...")
        st.session_state["tasks"] = clean_invalid_tasks(load_tasks())

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
            save_task(new_task, st.session_state["tasks"])  # Save task to JSON
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
