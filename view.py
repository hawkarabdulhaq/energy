import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def view_logs_page(log_data, task_data, sleep_data):
    """View Logs page with Plotly visualizations for Energy Levels, Activity Types, Task Weights, and Sleep Patterns."""
    st.title("📊 Daily Energy Levels, Tasks, and Sleep Logs")

    # Energy level mapping
    energy_mapping = {
        "Exhausted 😴": 1,
        "Fatigued 😓": 2,
        "Balanced 😐": 3,
        "Energized 🚀": 4,
        "Recharged 🌟": 5
    }

    # Convert data to DataFrames
    energy_df = pd.DataFrame(log_data) if log_data else pd.DataFrame(columns=["Time Block", "Energy Level", "Activity Type", "Timestamp"])
    task_df = pd.DataFrame(task_data) if task_data else pd.DataFrame(columns=["Task Type", "Task Length"])
    sleep_df = pd.DataFrame(sleep_data) if sleep_data else pd.DataFrame(columns=["Sleep Start", "Wake Up", "Duration (hrs)", "Timestamp"])

    # Ensure Timestamp column is datetime for energy and sleep logs
    if not energy_df.empty:
        energy_df["Timestamp"] = pd.to_datetime(energy_df["Timestamp"])
    if not sleep_df.empty:
        sleep_df["Timestamp"] = pd.to_datetime(sleep_df["Timestamp"])

    # Filter energy logs by selected date
    st.subheader("📅 Select a Date")
    if not energy_df.empty:
        available_dates = energy_df["Timestamp"].dt.date.unique()
        selected_date = st.selectbox("Choose a date", available_dates, key="select_date")

        # Filter data for the selected date
        day_energy_data = energy_df[energy_df["Timestamp"].dt.date == selected_date]
        selected_sleep_data = sleep_df[sleep_df["Timestamp"].dt.date == selected_date]

        if day_energy_data.empty:
            st.info(f"No energy logs available for {selected_date}.")
            return
    else:
        st.warning("⚠️ No energy logs available.")
        return

    # Map energy levels to numerical values and extract start hour
    day_energy_data["Energy Numeric"] = day_energy_data["Energy Level"].map(energy_mapping)
    day_energy_data["Start Hour"] = (
        day_energy_data["Time Block"].str.split("–").str[0].str.split(" ").str[0].astype(int)
    )

    # Sort data by Start Hour (early to late)
    day_energy_data = day_energy_data.sort_values(by="Start Hour")

    # Plotly chart
    fig = go.Figure()

    # Add energy data with Activity Type annotations
    fig.add_trace(go.Scatter(
        x=day_energy_data["Start Hour"],
        y=day_energy_data["Energy Numeric"],  # Mapped energy levels
        mode="lines+markers+text",
        name="Energy Levels",
        line=dict(color="rgba(38,198,218,1)", width=2),
        marker=dict(size=8),
        text=day_energy_data["Activity Type"],  # Display activity type on hover
        hovertemplate="<b>Hour:</b> %{x}:00<br>" +
                      "<b>Energy Level:</b> %{y}<br>" +
                      "<b>Activity:</b> %{text}<extra></extra>"
    ))

    # Add sleep data
    if not selected_sleep_data.empty:
        fig.add_trace(go.Scatter(
            x=[8],  # Replace with a meaningful sleep timeline, if available
            y=selected_sleep_data["Duration (hrs)"],
            mode="markers",
            name="Sleep Duration",
            marker=dict(color="rgba(255,99,132,1)", size=12),
            hovertemplate="<b>Duration:</b> %{y} hrs<extra></extra>"
        ))

    # Customize layout
    fig.update_layout(
        title="Energy Levels, Activities, and Sleep Patterns",
        xaxis_title="Hour of the Day",
        yaxis_title="Energy Levels (1-5) / Sleep Duration (hrs)",
        xaxis=dict(tickmode="linear", dtick=1),
        height=400,
        template="plotly_white"
    )

    # Render Plotly chart
    st.plotly_chart(fig, use_container_width=True)

    # Display Detailed Logs
    st.subheader("📋 Detailed Logs")

    # Display Energy Logs
    st.write("**Energy Logs**")
    st.dataframe(day_energy_data)

    # Display Task Logs
    st.write("**Task Logs**")
    if not task_df.empty:
        st.dataframe(task_df)
    else:
        st.info("No task logs recorded.")

    # Display Sleep Logs
    st.write("**Sleep Logs**")
    if not selected_sleep_data.empty:
        st.dataframe(selected_sleep_data)
    else:
        st.info("No sleep logs recorded for the selected date.")
