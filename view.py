import streamlit as st
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts

def view_logs_page(log_data, task_data, sleep_data):
    """View Logs page with a combo chart for Energy Levels, Task Weights, and Sleep Patterns."""
    st.title("📊 Daily Energy Levels, Tasks, and Sleep Logs")

    if not log_data:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
        return

    # Convert log data to DataFrame
    energy_df = pd.DataFrame(log_data)

    # Convert task data to DataFrame
    task_df = pd.DataFrame(task_data) if task_data else pd.DataFrame(columns=["Task Type", "Task Length"])

    # Convert sleep data to DataFrame
    sleep_df = pd.DataFrame(sleep_data) if sleep_data else pd.DataFrame(columns=["Sleep Start", "Wake Up", "Duration (hrs)", "Timestamp"])

    # Filter logs by selected date
    st.subheader("📅 Select a Date")
    energy_df["Timestamp"] = pd.to_datetime(energy_df["Timestamp"])
    available_dates = energy_df["Timestamp"].dt.date.unique()
    selected_date = st.selectbox("Choose a date to view your logs", available_dates, key="select_date")

    # Filter energy data for the selected date
    day_energy_data = energy_df[energy_df["Timestamp"].dt.date == selected_date]

    if day_energy_data.empty:
        st.info(f"No energy logs available for {selected_date}.")
        return

    # Filter sleep data for the selected date
    selected_sleep_data = sleep_df[sleep_df["Timestamp"].str.startswith(str(selected_date))] if not sleep_df.empty else pd.DataFrame()

    # Task data is not date-specific but can be used for visualization

    # Prepare Energy Series Data
    day_energy_data["Start Hour"] = (
        day_energy_data["Time Block"].str.split("–").str[0].str.split(" ").str[0].astype(int)
    )
    energy_series = [
        {"time": f"{hour}:00", "value": index}
        for hour, index in zip(day_energy_data["Start Hour"], day_energy_data.index)
    ]

    # Prepare Task Weight Data
    task_weight_series = [
        {"time": f"{hour}:00", "value": len(activity.split()) if isinstance(activity, str) else 0}
        for hour, activity in zip(day_energy_data["Start Hour"], day_energy_data["Activity Type"])
    ]

    # Prepare Sleep Series Data
    if not selected_sleep_data.empty:
        sleep_series = [
            {
                "time": f"{start}:00",
                "value": duration,
            }
            for start, duration in zip(
                selected_sleep_data["Sleep Start"], selected_sleep_data["Duration (hrs)"]
            )
        ]
    else:
        sleep_series = []

    # Combo Chart Options
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
        {
            "type": "Histogram",
            "data": task_weight_series,
            "options": {
                "color": "#26a69a",
                "priceFormat": {"type": "volume"},
                "priceScaleId": "",
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

    # Render Combo Chart
    st.subheader("🔋 Energy Levels, Task Weights, and Sleep Patterns")
    renderLightweightCharts(
        [{"chart": combo_chart_options, "series": combo_chart_series}], key="comboChart"
    )

    # Display Detailed Logs
    st.subheader("📋 Detailed Logs")

    # Display Energy Logs
    st.write("**Energy Logs**")
    st.dataframe(day_energy_data)

    # Display Task Logs
    st.write("**Task Logs**")
    if not task_df.empty:
        st.table(task_df)
    else:
        st.info("No task logs recorded.")

    # Display Sleep Logs
    st.write("**Sleep Logs**")
    if not selected_sleep_data.empty:
        st.table(selected_sleep_data)
    else:
        st.info("No sleep logs recorded for the selected date.")
