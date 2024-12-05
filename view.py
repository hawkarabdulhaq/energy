import streamlit as st
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts

def view_logs_page(log_data):
    """Enhanced View Logs page with a combo chart for Energy Levels and Task Weights."""
    st.title("📊 Daily Energy Levels and Tasks")

    if not log_data:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
        return

    # Convert log data to DataFrame
    df = pd.DataFrame(log_data)

    # Filter logs by selected date
    st.subheader("📅 Select a Date")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    available_dates = df["Timestamp"].dt.date.unique()
    selected_date = st.selectbox("Choose a date to view your logs", available_dates, key="select_date")

    day_data = df[df["Timestamp"].dt.date == selected_date]

    if day_data.empty:
        st.info(f"No logs available for {selected_date}.")
        return

    # Prepare data for the chart
    # Normalize time blocks to hours for simplicity (e.g., "6–8 AM" -> 6)
    day_data["Start Hour"] = day_data["Time Block"].str.split("–").str[0].str.split(" ").str[0].astype(int)

    # Sort by start hour to ensure correct order
    day_data = day_data.sort_values(by="Start Hour")

    # Prepare the series data
    energy_series = [
        {"time": str(hour), "value": energy}
        for hour, energy in zip(day_data["Start Hour"], day_data["Energy Level"])
    ]

    task_weight_series = [
        {"time": str(hour), "value": len(task.split()) if isinstance(task, str) else 0}
        for hour, task in zip(day_data["Start Hour"], day_data["Task"])
    ]

    # Chart options
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

    # Render the combo chart
    st.subheader("🔋 Energy Levels and Task Weights")
    renderLightweightCharts(
        [{"chart": combo_chart_options, "series": combo_chart_series}], key="energyTaskChart"
    )

    # Display the raw data table for transparency
    st.subheader("📋 Detailed Logs")
    st.dataframe(day_data)
