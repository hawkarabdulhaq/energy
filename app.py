import streamlit as st
import pandas as pd

# App Title
st.title("Energy Log App")

# Initialize session state for storing logs
if "data" not in st.session_state:
    st.session_state["data"] = []

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Log Energy", "View Logs"])

# Page 1: Log Energy
if page == "Log Energy":
    st.header("Log Your Energy Levels")

    # Time Block Selection as Buttons
    st.subheader("Select Time Block")
    time_blocks = ["6–8 AM", "8–10 AM", "10–12 PM", "12–2 PM", "2–4 PM", "4–6 PM", "6–8 PM"]
    selected_block = st.radio("Time Block", time_blocks, horizontal=True)

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
        # Append the entry to session state
        st.session_state["data"].append({
            "Time Block": selected_block,
            "Energy Level": energy_level,
            "Task": task,
            "Notes": notes
        })
        st.success("Entry saved!")
        # Clear inputs for better experience
        st.experimental_rerun()

# Page 2: View Logs
if page == "View Logs":
    st.header("Your Logged Entries")

    # Display logs if available
    if st.session_state["data"]:
        df = pd.DataFrame(st.session_state["data"])
        st.dataframe(df)
    else:
        st.write("No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
