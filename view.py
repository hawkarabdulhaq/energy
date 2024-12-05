import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_shap import st_shap
import shap

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

    # Waterfall-like Contribution Chart
    st.subheader("📊 Energy Level Contribution")
    contribution_df = (
        day_data.groupby("Activity Type")["Energy Level"]
        .mean()
        .reset_index()
        .sort_values(by="Energy Level", ascending=False)
    )
    contribution_df["Cumulative"] = contribution_df["Energy Level"].cumsum()

    fig_waterfall = px.bar(
        contribution_df,
        x="Activity Type",
        y="Energy Level",
        text="Energy Level",
        title="Activity Contribution to Energy Levels",
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)

    # Interactive Force Plot for Each Entry (SHAP-like visualization)
    st.subheader("💡 Detailed Insights for Each Entry")
    selected_entry_idx = st.selectbox("Select an entry to view details", day_data.index, format_func=lambda idx: f"Entry {idx + 1}")
    selected_entry = day_data.loc[selected_entry_idx]

    st.write(f"**Entry Details:**")
    st.json(selected_entry.to_dict(), expanded=True)

    # Simplified SHAP-like visualization (using dummy placeholders for SHAP)
    st.write("🔍 Energy Contributions (Simplified Visualization)")
    st_shap(
        shap.plots.waterfall(
            shap.Explanation(
                values=[selected_entry["Energy Level"]],
                base_values=selected_entry["Energy Level"] / 2,
                data=dict(selected_entry),
            )
        ),
        height=300,
    )

    # Display Detailed Data Table
    st.subheader("📋 Detailed Logs")
    st.dataframe(day_data)
