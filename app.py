import streamlit as st
import json
from datetime import datetime, timedelta
import time

def load_lottiefile(filepath: str):
    with open(filepath, "r") as file:
        return json.load(file)

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

    # Load and display a Lottie animation from a local file
    lottie_animation = load_lottiefile('energy/content/time.json')
    st_lottie(lottie_animation, speed=1, height=300, key="animation")

    # Countdown display
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        countdown_placeholder = st.empty()  # Placeholder for dynamic countdown

    st.markdown("<h2 style='color: red; text-align: center;'>Time left until registration closes:</h2>", unsafe_allow_html=True)
    countdown = calculate_time_difference()
    st.markdown(f"<h3 style='color: blue; text-align: center;'>{countdown}</h3>", unsafe_allow_html=True)
    
    # Course brief
    st.write("""
    Welcome to the early bird registration for our innovative course, "Personalized Training for Managing Your Time and Energy for Maximizing Your Impact and Production." 
    This course is delivered through Canvas and includes a mix of pre-recorded online sessions and interactive assignments. Additionally, you will receive personalized coaching to further enhance your learning experience. 
    Register now to take advantage of our 50% early bird discount. Normally priced at 195,000 Iraqi Dinar, you can enroll now for just 97,500 Iraqi Dinar. 
    This special offer is limited to the first 10 registrants, so secure your spot today!
    """)
    
    # Enrollment button
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfDyXAWlgczKY3mbYzlS1kVJtOUIetmYOI1wUOqx-qnAsMQAw/viewform?usp=sf_link"
    if st.button('Enroll Now', key="enroll", on_click=None, args=None, kwargs=None, help=None, disabled=False):
        st.markdown(f"<a style='display: block; text-align: center; background-color: orange; color: white; padding: 10px; border-radius: 5px; width: 100px; margin: auto;' href='{google_form_url}'>Go to Registration</a>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
