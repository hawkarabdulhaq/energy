import streamlit as st
from datetime import datetime, timedelta

def calculate_time_difference():
    # Set the target date and time for countdown (Year, Month, Day, Hour)
    target_date = datetime(2023, 11, 30, 0, 0, 0)  # Adjust the year if necessary
    now = datetime.now()
    diff = target_date - now
    if diff.total_seconds() > 0:
        return f"{diff.days} days, {diff.seconds//3600} hours, {(diff.seconds//60)%60} minutes"
    else:
        return "The countdown has ended!"

def main():
    st.title('Countdown to Course Registration Deadline')
    countdown = calculate_time_difference()
    st.header(f"Time left until registration closes: {countdown}")
    
    st.subheader("Limited Tickets Available for This Course!")
    st.write("Secure your spot now by enrolling early. Click the button below to go to the registration form.")
    
    # Link to your Google Form
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfDyXAWlgczKY3mbYzlS1kVJtOUIetmYOI1wUOqx-qnAsMQAw/viewform?usp=sf_link"
    if st.button('Enroll Now'):
        st.write(f"You are being redirected to the registration form.")
        st.markdown(f"[Click Here if you are not redirected]({google_form_url})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
