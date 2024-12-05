import streamlit as st
import pandas as pd
import plotly.express as px

def view_logs_page(log_data):
    """View Logs page with visualizations."""
    st.header("📊 Visualized Logs")

    if not log_data:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
        return

    # Convert log data to DataFrame
    df = pd.DataFrame(log_data)

    # Bar Chart: Frequency of Energy Levels
    st.subheader("🔋 Frequency of Energy Levels")
    energy_counts = df["Energy Level"].value_counts().reset_index()
    energy_counts.columns = ["Energy Level", "Count"]
    fig_bar = px.bar(
        energy_counts,
        x="Energy Level",
        y="Count",
        title="Frequency of Energy Levels",
        labels={"Count": "Frequency", "Energy Level": "Energy Level"},
        text="Count"
    )
    fig_bar.update_traces(textposition='outside')
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
        timeline_fig = px.scatter(
            df.sort_values("Timestamp"),
            x="Timestamp",
            y="Energy Level",
            color="Energy Level",
            title="Energy Levels Over Time",
            labels={"Energy Level": "Energy Level", "Timestamp": "Time"},
        )
        st.plotly_chart(timeline_fig, use_container_width=True)
    else:
        st.info("No timestamp data available.")
