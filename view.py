import streamlit as st
import pandas as pd
import plotly.express as px

def view_logs_page(log_data):
    """View Logs dashboard for a single day with multiple components."""
    st.header("📊 Daily Energy Dashboard")

    if not log_data:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
        return

    # Convert log data to DataFrame
    df = pd.DataFrame(log_data)

    # Filter logs by selected date
    st.subheader("📅 Select a Date")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    available_dates = df["Timestamp"].dt.date.unique()
    selected_date = st.selectbox("Choose a date", available_dates, key="select_date")

    day_data = df[df["Timestamp"].dt.date == selected_date]

    if day_data.empty:
        st.info(f"No logs available for {selected_date}.")
        return

    # 1. Bar Chart: Energy Levels by Time Block
    st.subheader("🔋 Energy Levels by Time Block")
    energy_by_time = day_data.groupby("Time Block")["Energy Level"].value_counts().unstack(fill_value=0).reset_index()
    fig_bar = px.bar(
        energy_by_time.melt(id_vars="Time Block", var_name="Energy Level", value_name="Count"),
        x="Time Block",
        y="Count",
        color="Energy Level",
        title="Energy Levels by Time Block",
        labels={"Count": "Frequency", "Time Block": "Time Block"},
        barmode="stack",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 2. Pie Chart: Activity Distribution
    st.subheader("🏷️ Activity Distribution")
    activity_counts = day_data["Activity Type"].value_counts().reset_index()
    activity_counts.columns = ["Activity Type", "Count"]
    fig_pie = px.pie(
        activity_counts,
        values="Count",
        names="Activity Type",
        title="Activity Distribution for the Day",
        hole=0.4,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # 3. Line Chart: Energy Levels Over Time
    st.subheader("⏱️ Energy Levels Throughout the Day")
    day_data_sorted = day_data.sort_values("Timestamp")
    fig_line = px.line(
        day_data_sorted,
        x="Timestamp",
        y="Energy Level",
        color="Energy Level",
        title="Energy Levels Over the Day",
        labels={"Energy Level": "Energy Level", "Timestamp": "Time"},
        markers=True,
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Summary Stats
    st.subheader("📊 Summary Statistics")
    avg_energy = day_data["Energy Level"].mode()[0]
    st.metric("Most Frequent Energy Level", avg_energy)

    top_activity = day_data["Activity Type"].mode()[0] if not day_data["Activity Type"].empty else "N/A"
    st.metric("Most Frequent Activity", top_activity)

    st.write("### Raw Data")
    st.dataframe(day_data)

