import streamlit as st
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts

def view_logs_page(log_data, task_data, sleep_data):
    """View Logs page for displaying Energy Levels, Task Logs, and Sleep Logs."""
    st.title("📊 Daily Energy, Tasks, and Sleep Patterns")

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

    # Prepare data for the chart
    day_energy_data["Start Hour"] = day_energy_data["Time Block"].str.split("–").str[0].str.split(" ").str[0].astype(int)
    energy_series = [{"time": f"{hour}:00", "value": idx + 1} for idx, hour in enumerate(day_energy_data["Start Hour"])]

    sleep_series = []
    if not selected_sleep_data.empty:
        sleep_series = [{"time": row["Sleep Start"], "value": row["Duration (hrs)"]} for _, row in selected_sleep_data.iterrows()]

    # Combo Chart Configuration
    combo_chart_options = {
        "height": 400,
        "rightPriceScale": {
            "scaleMargins": {"top": 0.2, "bottom": 0.25},
            "borderVisible": False,
        },
        "layout": {
            "background": {"type": "solid", "color": "#ffffff"},
            "textColor": "#000000",
        },
        "grid": {
            "vertLines": {"color": "rgba(42, 46, 57, 0)"},
            "horzLines": {"color": "rgba(42, 46, 57, 0.6)"},
        },
    }

    combo_chart_series = [
        {
            "type": "Area",
            "data": energy_series,
            "options": {
                "topColor": "rgba(38,198,218, 0.56)",
                "bottomColor": "rgba(38,198,218, 0.04)",
                "lineColor": "rgba(38,198,218, 1)",
                "lineWidth": 2,
            },
        },
    ]

    if sleep_series:
        combo_chart_series.append(
            {
                "type": "Line",
                "data": sleep_series,
                "options": {
                    "color": "rgba(255, 99, 132, 1)",
                    "lineWidth": 2,
                },
            }
        )

    # Render the chart
    st.subheader("🔋 Energy Levels and Sleep Patterns")
    try:
        renderLightweightCharts(
            [{"chart": combo_chart_options, "series": combo_chart_series}], key="comboChart"
        )
    except Exception as e:
        st.error(f"Error rendering chart: {e}")

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
