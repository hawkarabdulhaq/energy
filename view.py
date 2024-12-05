import streamlit as st
import pandas as pd

def view_logs_page(log_data, task_data, sleep_data):
    """Simplified View Logs page for displaying Energy, Task, and Sleep data."""
    st.title("📊 View Your Logs")

    # Convert data to DataFrames
    energy_df = pd.DataFrame(log_data) if log_data else pd.DataFrame(columns=["Time Block", "Energy Level", "Activity Type", "Timestamp"])
    task_df = pd.DataFrame(task_data) if task_data else pd.DataFrame(columns=["Task Type", "Task Length"])
    sleep_df = pd.DataFrame(sleep_data) if sleep_data else pd.DataFrame(columns=["Sleep Start", "Wake Up", "Duration (hrs)", "Timestamp"])

    # Display Energy Logs
    st.subheader("🔋 Energy Logs")
    if not energy_df.empty:
        energy_df["Timestamp"] = pd.to_datetime(energy_df["Timestamp"])
        st.dataframe(energy_df)
    else:
        st.info("No energy logs available.")

    # Display Task Logs
    st.subheader("📋 Task Logs")
    if not task_df.empty:
        st.dataframe(task_df)
    else:
        st.info("No task logs available.")

    # Display Sleep Logs
    st.subheader("🛌 Sleep Logs")
    if not sleep_df.empty:
        sleep_df["Timestamp"] = pd.to_datetime(sleep_df["Timestamp"])
        st.dataframe(sleep_df)
    else:
        st.info("No sleep logs available.")
