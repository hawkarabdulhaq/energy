import streamlit as st

def task_page():
    """Task Management Page."""
    st.title("📝 Task Management")

    # Example Task Input Form
    st.subheader("Add a New Task")
    task_name = st.text_input("Task Name", placeholder="Enter the task name...")
    task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    task_due_date = st.date_input("Due Date")

    # Save Task Button
    if st.button("Add Task"):
        if "tasks" not in st.session_state:
            st.session_state["tasks"] = []

        new_task = {
            "name": task_name,
            "priority": task_priority,
            "due_date": str(task_due_date),
        }
        st.session_state["tasks"].append(new_task)
        st.success("✅ Task added successfully!")

    # Display Current Tasks
    st.subheader("Your Tasks")
    if "tasks" in st.session_state and st.session_state["tasks"]:
        for task in st.session_state["tasks"]:
            st.write(f"- **{task['name']}** (Priority: {task['priority']}, Due: {task['due_date']})")
    else:
        st.info("No tasks added yet.")
