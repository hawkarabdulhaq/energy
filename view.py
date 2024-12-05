import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_shap import st_shap
import shap

# Sample Data: Complete one day's log
sample_log_data = [
    {"Time Block": "6–8 AM", "Energy Level": 2, "Activity Type": "Coffee Break", "Timestamp": "2024-12-05 05:42:09.120773"},
    {"Time Block": "6–8 AM", "Energy Level": 3, "Activity Type": "Planning", "Timestamp": "2024-12-05 05:46:05.791849"},
    {"Time Block": "8–10 AM", "Energy Level": 5, "Activity Type": "Studying", "Timestamp": "2024-12-05 08:10:53.848043"},
    {"Time Block": "10–12 PM", "Energy Level": 8, "Activity Type": "Brainstorming", "Timestamp": "2024-12-05 10:15:10.456789"},
    {"Time Block": "12–2 PM", "Energy Level": 9, "Activity Type": "Project Work", "Timestamp": "2024-12-05 12:45:20.789123"},
    {"Time Block": "2–4 PM", "Energy Level": 7, "Activity Type": "Workout", "Timestamp": "2024-12-05 14:05:40.373154"},
    {"Time Block": "4–6 PM", "Energy Level": 5, "Activity Type": "Emails & Admin", "Timestamp": "2024-12-05 16:22:33.456123"},
    {"Time Block": "6–8 PM", "Energy Level": 3, "Activity Type": "Dinner", "Timestamp": "2024-12-05 18:10:12.891234"},
    {"Time Block": "8–10 PM", "Energy Level": 6, "Activity Type": "Evening Walk", "Timestamp": "2024-12-05 20:05:00.123456"},
    {"Time Block": "10–12 PM", "Energy Level": 4, "Activity Type": "Reading", "Timestamp": "2024-12-05 22:30:45.789654"}
]

# Ensure session state contains log data
if "log_data" not in st.session_state:
    st.session_state["log_data"] = sample_log_data

# Define the View Logs Page
def view_logs_page(log_data):
    """Interactive View Logs page."""
    st.title("📊 Explore Your Daily Energy Logs")

    if not log_data:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
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

# Call the View Logs Page with session data
view_logs_page(st.session_state["log_data"])
