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

    # Select Sleep Start Time with Buttons
    st.subheader("1️⃣ What time did you go to sleep?")
    sleep_start_times = [f"{hour:02d}:00" for hour in range(18, 24)] + [f"{hour:02d}:00" for hour in range(0, 7)]
    selected_sleep_start = None

    cols = st.columns(len(sleep_start_times) // 2)
    for i, time in enumerate(sleep_start_times):
        if cols[i % len(cols)].button(time):
            st.session_state["selected_sleep_start"] = time

    if "selected_sleep_start" in st.session_state:
        selected_sleep_start = st.session_state["selected_sleep_start"]
        st.write(f"✅ **Selected Sleep Start Time:** {selected_sleep_start}")

    # Select Wake-Up Time with Buttons
    st.subheader("2️⃣ What time did you wake up?")
    wake_up_times = [f"{hour:02d}:00" for hour in range(4, 12)]
    selected_wake_up = None

    cols = st.columns(len(wake_up_times) // 2)
    for i, time in enumerate(wake_up_times):
        if cols[i % len(cols)].button(time):
            st.session_state["selected_wake_up"] = time

    if "selected_wake_up" in st.session_state:
        selected_wake_up = st.session_state["selected_wake_up"]
        st.write(f"✅ **Selected Wake-Up Time:** {selected_wake_up}")

    # Calculate Sleep Duration
    if selected_sleep_start and selected_wake_up:
        sleep_start = datetime.datetime.strptime(selected_sleep_start, "%H:%M").time()
        wake_up = datetime.datetime.strptime(selected_wake_up, "%H:%M").time()

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
                "Sleep Start": selected_sleep_start,
                "Wake Up": selected_wake_up,
                "Duration (hrs)": round(hours + minutes / 60, 2),
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
