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

    # Create placeholder elements for the countdown display
    countdown_placeholder = st.empty()
    st.subheader("Limited Tickets Available for This Course!")
    st.write("Secure your spot now by enrolling early. Click the button below to go to the registration form.")
    
    # Link to your Google Form
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfDyXAWlgczKY3mbYzlS1kVJtOUIetmYOI1wUOqx-qnAsMQAw/viewform?usp=sf_link"
    enroll_button = st.button('Enroll Now')
    
    # Update the countdown every second
    while True:
        countdown = calculate_time_difference()
        countdown_placeholder.markdown(f"### Time left until registration closes: {countdown}")
        if enroll_button:
            st.write(f"You are being redirected to the registration form.")
            st.markdown(f"[Click Here if you are not redirected]({google_form_url})", unsafe_allow_html=True)
        time.sleep(1)

if __name__ == "__main__":
    main()
