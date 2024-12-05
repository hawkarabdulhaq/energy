import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def view_logs_page(log_data):
    """View Logs page with visualizations."""
    st.header("📊 Visualized Logs")

    if not log_data:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
        return

    # Convert log data to DataFrame
    df = pd.DataFrame(log_data)

    # Bar Chart: Energy Levels by Time Block
    st.subheader("🔋 Energy Levels by Time Block")
    energy_by_time = df.groupby("Time Block")["Energy Level"].mean().reset_index()
    fig_bar = px.bar(
        energy_by_time,
        x="Time Block",
        y="Energy Level",
        title="Average Energy Levels by Time Block",
        labels={"Energy Level": "Average Energy Level", "Time Block": "Time Block"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Pie Chart: Activity Distribution
    st.subheader("🏷️ Activity Distribution")
    if "Activity Type" in df.columns:
        activity_counts = df["Activity Type"].value_counts().reset_index()
        activity_counts.columns = ["Activity Type", "Count"]
        fig_pie = px.pie(
            activity_counts,
            values="Count",
            names="Activity Type",
            title="Distribution of Activities",
            hole=0.4,
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No activity data available.")

    # Timeline: Energy Levels Throughout the Day
    st.subheader("⏱️ Energy Levels Throughout the Day")
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        timeline_fig = px.line(
            df.sort_values("Timestamp"),
            x="Timestamp",
            y="Energy Level",
            title="Energy Levels Over Time",
            markers=True,
            labels={"Energy Level": "Energy Level", "Timestamp": "Time"},
        )
        st.plotly_chart(timeline_fig, use_container_width=True)
    else:
        st.info("No timestamp data available.")
