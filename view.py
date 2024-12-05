import streamlit as st
import pandas as pd


def view_logs_page(log_data):
    """View Logs page logic."""
    st.header("📊 Your Logged Entries")

    # Display logs in a table if available
    if log_data:
        df = pd.DataFrame(log_data)
        st.dataframe(df)
    else:
        st.warning("⚠️ No entries logged yet. Go to the 'Log Energy' page to add your first entry.")
