import streamlit as st
import datetime
from activity import get_activity_types  # Import activity types from activity.py

# Helper Functions
def save_log(log_entry, log_data, save_to_local):
    """Save a single log entry."""
    log_data.append(log_entry)
    save_to_local(log_data)
    return log_data


def log_energy_page(log_data, save_to_local):
    """Log Energy page logic."""
    st.header("Log Your Energy Levels")

    # Step 1: Time Block Selection
    st.subheader("1️⃣ Select Time Block")
    time_blocks = ["6–8 AM", "8–10 AM", "10–12 PM", "12–2 PM", "2–4 PM", "4–6 PM", "6–8 PM"]

    # Display buttons for time block selection
    time_block_cols = st.columns(len(time_blocks))
    for i, block in enumerate(time_blocks):
        if time_block_cols[i].button(block):
            st.session_state["selected_block"] = block

    # Show selected time block
    if st.session_state.get("selected_block"):
        st.write(f"✅ **Selected Time Block:** {st.session_state['selected_block']}")

    # Step 2: Energy Level Slider
    st.subheader("2️⃣ Rate Your Energy Level")
    energy_level = st.slider("Rate your energy level (1-10)", 1, 10, 5)

    # Step 3: Activity Type Selection with Buttons
    st.subheader("3️⃣ Select Activity Type")
    activity_categories = get_activity_types()  # Fetch activity categories

    for category, activities in activity_categories.items():
        st.markdown(f"**{category}**")
        activity_cols = st.columns(len(activities))
        for i, activity in enumerate(activities):
            if activity_cols[i].button(activity):
                st.session_state["selected_activity"] = activity

    # Show selected activity
    if st.session_state.get("selected_activity"):
        st.write(f"✅ **Selected Activity:** {st.session_state['selected_activity']}")

    # Step 4: Additional Details (Optional)
    st.subheader("4️⃣ Additional Details")
    task = st.text_input("Add more details about the activity (optional):")

    # Step 5: Notes (Optional)
    st.subheader("5️⃣ Notes")
    notes = st.text_area("Add any notes or observations (optional):")

    # Save Entry Button
    if st.button("Save Entry"):
        if st.session_state.get("selected_block") and st.session_state.get("selected_activity"):
            new_entry = {
                "Time Block": st.session_state["selected_block"],
                "Energy Level": energy_level,
                "Activity Type": st.session_state["selected_activity"],
                "Task": task,
                "Notes": notes,
                "Timestamp": str(datetime.datetime.now()),
            }
            save_log(new_entry, log_data, save_to_local)
            st.success("🚀 Entry saved successfully!")
            # Reset selections
            st.session_state["selected_block"] = None
            st.session_state["selected_activity"] = None
        else:
            st.error("❌ Please select both a time block and an activity before saving.")
