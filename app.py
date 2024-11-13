import streamlit as st
from datetime import datetime, timedelta

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
        return f"{days}:{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return "00:00:00:00"

def main():
    st.title('Countdown to Course Registration Deadline')
    
    countdown = calculate_time_difference()
    st.subheader("Time left until registration closes:")
    # Create a column layout to display the countdown in a table-like format
    col1, col2, col3, col4 = st.columns(4)
    days, hours, minutes, seconds = countdown.split(':')
    with col1:
        st.metric(label="Days", value=days)
    with col2:
        st.metric(label="Hours", value=hours)
    with col3:
        st.metric(label="Minutes", value=minutes)
    with col4:
        st.metric(label="Seconds", value=seconds)
    
    st.subheader("Limited Tickets Available for This Course!")
    st.write("Secure your spot now by enrolling early. Click the button below to go to the registration form.")
    
    # Link to your Google Form
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfDyXAWlgczKY3mbYzlS1kVJtOUIetmYOI1wUOqx-qnAsMQAw/viewform?usp=sf_link"
    if st.button('Enroll Now'):
        st.write(f"You are being redirected to the registration form.")
        st.markdown(f"[Click Here if you are not redirected]({google_form_url})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
