import streamlit as st
from datetime import datetime, timedelta
import time

def calculate_time_difference():
    # Set the target date and time for countdown
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
    st.set_page_config(page_title="Early Bird Registration", page_icon=":alarm_clock:")
    st.title('Early Bird Registration for Personalized Training for Managing Your Time and Energy')

    # Description text
    st.write("""
    Welcome to the early bird registration for our innovative course, "Personalized Training for Managing Your Time and Energy for Maximizing Your Impact and Production." 
    This course is delivered through Canvas and includes a mix of pre-recorded online sessions and interactive assignments. Additionally, you will receive personalized coaching to further enhance your learning experience. 
    Register now to take advantage of our 50% early bird discount. Normally priced at 195,000 Iraqi Dinar, you can enroll now for just 97,500 Iraqi Dinar. 
    This special offer is limited to the first 10 registrants, so secure your spot today!
    """)
    
    # Using columns to center the countdown display
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        countdown_placeholder = st.empty()  # Placeholder for dynamic countdown
    
    # Link to your Google Form
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfDyXAWlgczKY3mbYzlS1kVJtOUIetmYOI1wUOqx-qnAsMQAw/viewform?usp=sf_link"
    if st.button('Enroll Now', key="enroll"):
        st.write("You are being redirected to the registration form.")
        st.markdown(f"[Click Here if you are not redirected]({google_form_url})", unsafe_allow_html=True)
    
    # Update the countdown every second
    while True:
        countdown = calculate_time_difference()
        countdown_placeholder.markdown(f"<h1 style='text-align: center; font-size: 48px;'>Time left until registration closes: {countdown}</h1>", unsafe_allow_html=True)
        time.sleep(1)

if __name__ == "__main__":
    main()
