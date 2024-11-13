import streamlit as st
from datetime import datetime, timedelta
import time

def calculate_time_difference():
    # Set the target date and time for countdown (Year, Month, Day, Hour)
    target_date = datetime(2024, 11, 30, 0, 0, 0)
    now = datetime.now()
    diff = target_date - now
    if diff.total_seconds() > 0:
        # Calculate days, hours, minutes, and seconds
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return "00:00:00:00"

def main():
    st.title('Countdown to Course Registration Deadline')
    
    # Using columns to center the countdown display
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        countdown_placeholder = st.empty()  # Placeholder for dynamic countdown

    st.subheader("Limited Tickets Available for This Course!")
    st.write("Secure your spot now by enrolling early. Click the button below to go to the registration form.")
    
    # Link to your Google Form
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfDyXAWlgczKY3mbYzlS1kVJtOUIetmYOI1wUOqx-qnAsMQAw/viewform?usp=sf_link"
    if st.button('Enroll Now', key="enroll"):
        st.write(f"You are being redirected to the registration form.")
        st.markdown(f"[Click Here if you are not redirected]({google_form_url})", unsafe_allow_html=True)
    
    # Update the countdown every second
    while True:
        countdown = calculate_time_difference()
        countdown_placeholder.markdown(f"<h1 style='text-align: center; font-size: 48px;'>Time left until registration closes: {countdown}</h1>", unsafe_allow_html=True)
        time.sleep(1)

if __name__ == "__main__":
    main()
