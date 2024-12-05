import streamlit as st
import pandas as pd

# App Title
st.title("Energy Log App")

# Initialize session state for storing logs and navigation
if "data" not in st.session_state:
    st.session_state["data"] = []
if "page" not in st.session_state:
    st.session_state["page"] = "Log Energy"  # Default page
if "selected_block" not in st.session_state:
    st.session_state["selected_block"] = None

# Sidebar for Navigation with Buttons
st.sidebar.title("Navigation")
if st.sidebar.button("Log Energy"):
    st.session_state["page"] = "Log Energy"
if st.sidebar.button("View Logs"):
    st.session_state["page"] = "View Logs"

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
            # Append the entry to session state
            st.session_state["data"].append({
                "Time Block": st.session_state["selected_block"],
                "Energy Level": energy_level,
                "Task": task,
                "Notes": notes
            })
            st.success("Entry saved!")
            # Reset selected block for a fresh start
            st.session_state["selected_block"] = None
            st.experimental_rerun()
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
