import streamlit as st

def task_page():
    """Task Management Page."""
    st.title("📝 Task Management")

    # Step 1: Select Task Type
    st.subheader("1️⃣ Select Task Type")
    task_types = ["Data Processing", "Writing", "Analysis", "Meeting", "Coding", "Design"]
    selected_task_type = None

    cols = st.columns(len(task_types))
    for i, task_type in enumerate(task_types):
        if cols[i].button(task_type, key=f"task_type_{task_type}"):
            st.session_state["selected_task_type"] = task_type

    if "selected_task_type" in st.session_state:
        selected_task_type = st.session_state["selected_task_type"]
        st.write(f"✅ **Selected Task Type:** {selected_task_type}")

    # Step 2: Select Task Length
    st.subheader("2️⃣ Select Task Length")
    task_lengths = ["Full Day Task", "Half Day Task", "Few Hours Task", "Less than 1 Hour"]
    selected_task_length = None

    cols = st.columns(len(task_lengths))
    for i, task_length in enumerate(task_lengths):
        if cols[i].button(task_length, key=f"task_length_{task_length}"):
            st.session_state["selected_task_length"] = task_length

    if "selected_task_length" in st.session_state:
        selected_task_length = st.session_state["selected_task_length"]
        st.write(f"✅ **Selected Task Length:** {selected_task_length}")

    # Step 3: Quantitative Inputs
    st.subheader("3️⃣ Quantify the Task")
    task_effort = st.slider("Estimated Effort (Hours)", 1, 10, 5, key="task_effort")  # Slider for hours
    task_priority = st.radio("Task Priority", ["Low", "Medium", "High"], key="task_priority")  # Priority options
    task_weight = st.number_input("Task Weight (e.g., Importance or Difficulty)", min_value=1, max_value=10, value=5, key="task_weight")  # Numeric scale

    # Save Task Button
    if st.button("Save Task", key="save_task"):
        if "tasks" not in st.session_state:
            st.session_state["tasks"] = []

        if selected_task_type and selected_task_length:
            new_task = {
                "Task Type": selected_task_type,
                "Task Length": selected_task_length,
                "Effort (Hours)": task_effort,
                "Priority": task_priority,
                "Weight": task_weight,
            }
            st.session_state["tasks"].append(new_task)
            st.success("✅ Task saved successfully!")
            # Reset selected task type and length
            st.session_state["selected_task_type"] = None
            st.session_state["selected_task_length"] = None
        else:
            st.error("❌ Please select both a task type and a task length before saving.")

    # Step 4: View Saved Tasks
    st.subheader("📋 Your Saved Tasks")
    if "tasks" in st.session_state and st.session_state["tasks"]:
        for task in st.session_state["tasks"]:
            st.write(
                f"- **{task['Task Type']}** ({task['Task Length']}, {task['Priority']} Priority)\n"
                f"  - Effort: {task['Effort (Hours)']} hrs, Weight: {task['Weight']}"
            )
    else:
        st.info("No tasks saved yet. Start adding tasks above!")
