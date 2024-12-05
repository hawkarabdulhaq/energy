import streamlit as st
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts

def view_logs_page(log_data, task_data, sleep_data):
    """View Logs page with a combo chart for Energy Levels, Task Weights, and Sleep Patterns."""
    st.title("📊 Daily Energy Levels, Tasks, and Sleep Logs")

    # Check if energy data is available
    if not log_data:
        st.warning("⚠️ No energy entries logged yet. Go to the 'Log Energy' page to add your first entry.")
        return

    # Convert energy log data to DataFrame
    energy_df = pd.DataFrame(log_data)

    # Convert task data to DataFrame
    task_df = pd.DataFrame(task_data) if task_data else pd.DataFrame(columns=["Task Type", "Task Length"])

    # Convert sleep data to DataFrame
    sleep_df = pd.DataFrame(sleep_data) if sleep_data else pd.DataFrame(columns=["Sleep Start", "Wake Up", "Duration (hrs)", "Timestamp"])

    # Filter energy logs by selected date
    st.subheader("📅 Select a Date")
    energy_df["Timestamp"] = pd.to_datetime(energy_df["Timestamp"])
    available_dates = energy_df["Timestamp"].dt.date.unique()
    selected_date = st.selectbox("Choose a date to view your logs", available_dates, key="select_date")

    # Filter energy logs for the selected date
    day_energy_data = energy_df[energy_df["Timestamp"].dt.date == selected_date]

    if day_energy_data.empty:
        st.info(f"No energy logs available for {selected_date}.")
        return

    # Filter sleep logs for the selected date
    sleep_df["Timestamp"] = pd.to_datetime(sleep_df["Timestamp"])
    selected_sleep_data = sleep_df[sleep_df["Timestamp"].dt.date == selected_date]

    # Task data is not date-specific; display all tasks

    # Prepare Energy Series Data
    try:
        day_energy_data["Start Hour"] = (
            day_energy_data["Time Block"].str.split("–").str[0].str.split(" ").str[0].astype(int)
        )
        energy_series = [
            {"time": f"{hour}:00", "value": i + 1}
            for hour, i in zip(day_energy_data["Start Hour"], range(len(day_energy_data)))
        ]
    except Exception as e:
        st.error(f"Error preparing energy data for the chart: {e}")
        return

    # Prepare Task Weight Data
    try:
        task_weight_series = [
            {"time": f"{hour}:00", "value": len(activity.split()) if isinstance(activity, str) else 0}
            for hour, activity in zip(day_energy_data["Start Hour"], day_energy_data["Activity Type"])
        ]
    except Exception as e:
        st.error(f"Error preparing task weight data for the chart: {e}")
        return

    # Prepare Sleep Series Data
    try:
        if not selected_sleep_data.empty:
            sleep_series = [
                {
                    "time": sleep_start,
                    "value": duration,
                }
                for sleep_start, duration in zip(selected_sleep_data["Sleep Start"], selected_sleep_data["Duration (hrs)"])
            ]
        else:
            sleep_series = []
    except Exception as e:
        st.error(f"Error preparing sleep data for the chart: {e}")
        return

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
    try:
        renderLightweightCharts(
            [{"chart": combo_chart_options, "series": combo_chart_series}], key="comboChart"
        )
    except Exception as e:
        st.error(f"Error rendering the chart: {e}")

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
