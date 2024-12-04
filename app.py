import streamlit as st
from utils.authentication import authenticate_user, create_user
from utils.data_handler import load_user_data, save_user_data
import os

# App title
st.title("Energy Log App")

# Authentication
st.sidebar.title("Sign In or Register")
action = st.sidebar.radio("Action", ["Sign In", "Register"])

if action == "Register":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Register"):
        if create_user(username, password):
            st.sidebar.success("User registered successfully. Please sign in.")
        else:
            st.sidebar.error("Username already exists. Please choose a different one.")
elif action == "Sign In":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Sign In"):
        if authenticate_user(username, password):
            st.sidebar.success("Welcome, " + username)
            # Main app logic
            st.subheader(f"Hello, {username}! Log Your Energy Levels Below.")
            data = load_user_data(username)
            
            # Log energy data
            time_block = st.selectbox("Select Time Block", ["6–8 AM", "8–10 AM", "10–12 PM", "12–2 PM", "2–4 PM", "4–6 PM", "6–8 PM"])
            energy_level = st.slider("Energy Level (1-10)", 1, 10)
            task = st.text_input("What task did you do?")
            notes = st.text_area("Additional Notes (optional)")

            if st.button("Save Entry"):
                data.append({"time_block": time_block, "energy_level": energy_level, "task": task, "notes": notes})
                save_user_data(username, data)
                st.success("Entry saved!")

            # Display daily entries
            st.subheader("Your Daily Entries")
            for entry in data:
                st.write(f"**{entry['time_block']}**: Energy {entry['energy_level']}/10 | Task: {entry['task']} | Notes: {entry.get('notes', 'N/A')}")

        else:
            st.sidebar.error("Invalid username or password. Please try again.")
