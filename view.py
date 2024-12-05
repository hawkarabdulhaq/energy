import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_shap import st_shap
import shap
import json
import os

# Define file path
LOG_FILE_PATH = "database/energy_logs.json"

# Helper Function to Load Data
def load_logs():
    """Load logs from the JSON file."""
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, "r") as file:
            return json.load(file)
    else:
        st.error(f"Log file not found: {LOG_FILE_PATH}")
        return []

# Define the View Logs Page
def view_logs_page():
    """Interactive View Logs page."""
    st.title("📊 Explore Your Daily Energy Logs")

    # Fetch log data
    log_data = load_logs()

    if not log_data:
        st.warning("⚠️ No entries logged yet. Please add logs to the database.")
        return

    # Convert log data to DataFrame
    df = pd.DataFrame(log_data)

    # Filter logs by selected date
    st.subheader("📅 Filter by Date")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    available_dates = df["Timestamp"].dt.date.unique()
    selected_date = st.selectbox("Choose a date to view your logs", available_dates, key="select_date")

    day_data = df[df["Timestamp"].dt.date == selected_date]

    if day_data.empty:
        st.info(f"No logs available for {selected_date}.")
        return

    # Summary Metrics
    st.subheader("📋 Daily Summary")
    total_entries = len(day_data)
    avg_energy = round(day_data["Energy Level"].mean(), 1)
    most_frequent_activity = day_data["Activity Type"].mode()[0] if not day_data["Activity Type"].mode().empty else "None"

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Entries", total_entries, help="Total number of logs for the day.")
    col2.metric("Average Energy Level", avg_energy, help="Average energy level across logs.")
    col3.metric("Most Frequent Activity", most_frequent_activity, help="The activity logged most often.")

    # Beeswarm-style Activity Chart
    st.subheader("🎨 Activity Levels")
    beeswarm_data = day_data[["Time Block", "Energy Level", "Activity Type"]]
    beeswarm_data["Time Block (ordinal)"] = pd.Categorical(beeswarm_data["Time Block"], ordered=True)
    fig_beeswarm = px.strip(
        beeswarm_data,
        x="Time Block (ordinal)",
        y="Energy Level",
        color="Activity Type",
        title="Energy Levels Across Time Blocks",
        labels={"Time Block (ordinal)": "Time Block", "Energy Level": "Energy Level"},
        hover_data=["Activity Type"],
    )
    st.plotly_chart(fig_beeswarm, use_container_width=True)

    # Display Detailed Data Table
    st.subheader("📋 Detailed Logs")
    st.dataframe(day_data)

# Call the View Logs Page
if __name__ == "__main__":
    view_logs_page()
