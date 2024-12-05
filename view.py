import streamlit as st
import pandas as pd

def view_logs_page(log_data, task_data, sleep_data):
    """Simplified View Logs page for displaying Energy, Task, and Sleep data."""
    st.title("📊 View Your Logs")

    # Convert data to DataFrames
    st.write("DEBUG: Converting log_data to DataFrame.")
    energy_df = pd.DataFrame(log_data) if log_data else pd.DataFrame(columns=["Time Block", "Energy Level", "Activity Type", "Timestamp"])
    st.write("DEBUG: Converted energy_df:", energy_df)

    st.write("DEBUG: Converting task_data to DataFrame.")
    task_df = pd.DataFrame(task_data) if task_data else pd.DataFrame(columns=["Task Type", "Task Length"])
    st.write("DEBUG: Converted task_df:", task_df)

    st.write("DEBUG: Converting sleep_data to DataFrame.")
    sleep_df = pd.DataFrame(sleep_data) if sleep_data else pd.DataFrame(columns=["Sleep Start", "Wake Up", "Duration (hrs)", "Timestamp"])
    st.write("DEBUG: Converted sleep_df:", sleep_df)

    # Display Energy Logs
    st.subheader("🔋 Energy Logs")
    if not energy_df.empty:
        st.write("DEBUG: Parsing 'Timestamp' column in energy_df.")
        energy_df["Timestamp"] = pd.to_datetime(energy_df["Timestamp"], errors="coerce")
        st.write("DEBUG: Parsed energy_df:", energy_df)
        st.dataframe(energy_df)
    else:
        st.info("No energy logs available.")
        st.write("DEBUG: energy_df is empty.")

    # Display Task Logs
    st.subheader("📋 Task Logs")
    if not task_df.empty:
        st.write("DEBUG: task_df contains data:", task_df)
        st.dataframe(task_df)
    else:
        st.info("No task logs available.")
        st.write("DEBUG: task_df is empty.")

    # Display Sleep Logs
    st.subheader("🛌 Sleep Logs")
    if not sleep_df.empty:
        st.write("DEBUG: Parsing 'Timestamp' column in sleep_df.")
        sleep_df["Timestamp"] = pd.to_datetime(sleep_df["Timestamp"], errors="coerce")
        st.write("DEBUG: Parsed sleep_df:", sleep_df)
        st.dataframe(sleep_df)
    else:
        st.info("No sleep logs available.")
        st.write("DEBUG: sleep_df is empty.")
