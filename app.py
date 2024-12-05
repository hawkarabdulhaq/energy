import streamlit as st
import pandas as pd

# App Title
st.title("Energy Log App")

# Initialize an empty data structure for logging
if "data" not in st.session_state:
    st.session_state["data"] = []

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Log Energy", "View Logs"])

# Page 1: Log Energy
if page == "Log Energy":
    st.header("Log Your Energy Levels")
    
    # Input Fields
    time_block = st.selectbox("Select Time Block", ["6–8 AM", "8–10 AM", "10–12 PM", "12–2 PM", "2–4 PM", "4–6 PM", "6–8 PM"])
    energy_level = st.slider("Energy Level (1-10)", 1, 10, 5)
    task = st.text_input("What task did you do?")
    notes = st.text_area("Additional Notes (optional)")

    # Button to save log
    if st.button("Save Entry"):
        st.session_state["data"].append({
            "Time Block": time_block,
            "Energy Level": energy_level,
            "Task": task,
            "Notes": notes
        })
        st.success("Entry saved!")

# Page 2: View Logs
if page == "View Logs":
    st.header("Your Logged Entries")
    
    # Display logs if available
    if st.session_state["data"]:
        df = pd.DataFrame(st.session_state["data"])
        st.dataframe(df)
    else:
        st.write("No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
