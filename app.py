import streamlit as st
from streamlit_lottie import st_lottie
import json
from datetime import datetime, timedelta
import time

# Function to load a local Lottie file
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as file:
        return json.load(file)

def calculate_time_difference():
    target_date = datetime(2024, 11, 30, 0, 0, 0)
    now = datetime.now()
    diff = target_date - now
    if diff.total_seconds() > 0:
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return "00:00:00:00"

def main():
    st.set_page_config(page_title="Early Bird Registration", page_icon=":alarm_clock:")
    st.title('Early Bird Course Registration')

    # Load and display a Lottie animation from a local file
    lottie_animation = load_lottiefile('content/time.json')
    st_lottie(lottie_animation, speed=1, height=300, key="animation")

    # Display the countdown
    st.markdown("<h1 style='color: black; text-align: center; font-family: Courier;'>Registration closes in:</h1>", unsafe_allow_html=True)
    countdown = calculate_time_difference()
    st.markdown(f"<h2 style='text-align: center; font-size: 48px; color: red; font-weight: bold; font-family: Courier;'>{countdown}</h2>", unsafe_allow_html=True)

    # Course brief
    st.write("""
    Welcome to the early bird registration for "Personalized Training for Managing Your Time and Energy." 
    This innovative course includes pre-recorded sessions, interactive assignments, and personalized coaching.
    Register now to secure your spot at a 50% discount—only 97,500 Iraqi Dinar!
    """, style={'font-family': 'Courier'})

    # Enrollment button
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfDyXAWlgczKY3mbYzlS1kVJtOUIetmYOI1wUOqx-qnAsMQAw/viewform?usp=sf_link"
    if st.button('Enroll Now', key="enroll", on_click=None, args=None, kwargs=None, help=None, disabled=False):
        st.markdown(f"<a style='display: block; text-align: center; background-color: orange; color: white; padding: 10px; border-radius: 5px; width: 100px; margin: auto; font-family: Courier;' href='{google_form_url}'>Go to Registration</a>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
