import streamlit as st
import datetime

# Helper Functions
def save_sleep_data(data):
    """Save sleep data to session state."""
    if "sleep_data" not in st.session_state:
        st.session_state["sleep_data"] = []
    st.session_state["sleep_data"].append(data)

def get_sleep_data():
    """Retrieve saved sleep data."""
    if "sleep_data" in st.session_state:
        return st.session_state["sleep_data"]
    return []

# Sleep Page
def sleep_page():
    st.title("🌙 Sleep Log")

    # Input for Sleep Start Time
    st.subheader("Log Your Sleeping Hours")
    sleep_start = st.time_input("What time did you go to sleep?", datetime.time(22, 0))
    
    # Input for Wake-Up Time
    wake_up = st.time_input("What time did you wake up?", datetime.time(6, 0))

    # Calculate Sleep Duration
    if wake_up > sleep_start:
        sleep_duration = datetime.datetime.combine(datetime.date.today(), wake_up) - datetime.datetime.combine(datetime.date.today(), sleep_start)
    else:
        sleep_duration = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), wake_up) - datetime.datetime.combine(datetime.date.today(), sleep_start)
    
    # Display Sleep Duration
    hours, remainder = divmod(sleep_duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    st.write(f"🕒 You slept for **{hours} hours and {minutes} minutes**.")

    # Button to Save Sleep Data
    if st.button("Save Sleep Log"):
        sleep_entry = {
            "Sleep Start": str(sleep_start),
            "Wake Up": str(wake_up),
            "Duration (hrs)": hours + minutes / 60,
            "Timestamp": str(datetime.datetime.now())
        }
        save_sleep_data(sleep_entry)
        st.success("✅ Sleep log saved successfully!")

    # Display Saved Sleep Data
    st.subheader("Your Sleep Records")
    sleep_data = get_sleep_data()
    if sleep_data:
        st.table(sleep_data)
    else:
        st.info("No sleep logs recorded yet. Start logging your sleep above.")
