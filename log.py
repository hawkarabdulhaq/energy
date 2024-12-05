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

    # Step 2: Energy Level Selection with Descriptive Buttons
    st.subheader("2️⃣ How do you feel?")
    energy_levels = [
    "Exhausted 😴",      # Low energy, feeling drained
    "Fatigued 😓",       # Slightly higher than exhausted
    "Balanced 😐",       # Neutral energy, steady state
    "Energized 🚀",      # Positive, ready to work
    "Recharged 🌟"       # Fully refreshed and motivated
    ]

    cols = st.columns(len(energy_levels))
    for i, level in enumerate(energy_levels):
        if cols[i].button(level, key=f"energy_{level}"):
            st.session_state["selected_energy_level"] = level

    # Show selected energy level
    if st.session_state.get("selected_energy_level"):
        st.write(f"✅ **Selected Energy Level:** {st.session_state['selected_energy_level']}")

    # Step 3: Activity Type Selection
    st.subheader("3️⃣ Select Activity Type")
    activity_categories = get_activity_types()  # Fetch activity categories

    # Group buttons under collapsible sections
    selected_activity = None
    for category, activities in activity_categories.items():
        with st.expander(f"**{category}**"):
            cols = st.columns(len(activities))
            for i, activity in enumerate(activities):
                if cols[i % len(cols)].button(activity, key=f"activity_{activity}"):
                    selected_activity = activity
                    st.session_state["selected_activity"] = selected_activity
                    st.write(f"✅ **You selected:** {selected_activity}")

    # Save Entry Button
    if st.button("Save Entry"):
        if st.session_state.get("selected_block") and st.session_state.get("selected_energy_level") and st.session_state.get("selected_activity"):
            new_entry = {
                "Time Block": st.session_state["selected_block"],
                "Energy Level": st.session_state["selected_energy_level"],
                "Activity Type": st.session_state["selected_activity"],
                "Timestamp": str(datetime.datetime.now()),
            }
            save_log(new_entry, log_data, save_to_local)
            st.success("🚀 Entry saved successfully!")
            # Reset selections
            st.session_state["selected_block"] = None
            st.session_state["selected_energy_level"] = None
            st.session_state["selected_activity"] = None
        else:
            st.error("❌ Please select a time block, energy level, and activity before saving.")
