import streamlit as st
from streamlit_lottie import st_lottie  # Import st_lottie from streamlit_lottie
import json
from datetime import datetime
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
    
    # Title with font set to Courier and justified text alignment
    st.markdown("""
    <h1 style='text-align: justify; font-family: Courier;'>
    Early Bird Registration for Personalized Training for Managing Your Time and Energy
    </h1>
    <p style='font-family: Courier;'>Course by <a href='https://hawkardemo.streamlit.app/' target='_blank'>Hawkar Ali Abdulhaq</a></p>
    """, unsafe_allow_html=True)

    # Load and display the Lottie animation from a local file
    lottie_animation = load_lottiefile('content/time.json')
    st_lottie(lottie_animation, speed=1, height=300, key="animation")

    # Live countdown display with the timer in red and bold, using Courier font
    countdown_placeholder = st.empty()
    st.markdown("<p style='font-family: Courier; text-align: center; font-size: 24px;'>Time left until registration closes:</p>", unsafe_allow_html=True)
    
    while True:
        countdown = calculate_time_difference()
        countdown_placeholder.markdown(f"<p style='font-family: Courier; text-align: center; font-size: 48px; color: red; font-weight: bold;'>{countdown}</p>", unsafe_allow_html=True)
        time.sleep(1)  # Update every second

    # Course description, start date, and pricing information, all in black with Courier font
    st.markdown("""
    <p style='font-family: Courier;'>
    Welcome to the early bird registration for our innovative course, "Personalized Training for Managing Your Time and Energy for Maximizing Your Impact and Production." 
    This course is delivered through Canvas and includes a mix of pre-recorded online sessions and interactive assignments. Additionally, you will receive personalized coaching to further enhance your learning experience.
    Register now to take advantage of our 50% early bird discount. Normally priced at 195,000 Iraqi Dinar, you can enroll now for just 97,500 Iraqi Dinar.
    This special offer is limited to the first 10 registrants, so secure your spot today!
    <strong>The course will start on 1st December 2024.</strong>
    </p>
    """, unsafe_allow_html=True)

    # Enrollment button
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfDyXAWlgczKY3mbYzlS1kVJtOUIetmYOI1wUOqx-qnAsMQAw/viewform?usp=sf_link"
    st.markdown(f"""
    <a style='display: block; text-align: center; background-color: orange; color: white; padding: 10px; border-radius: 5px; width: 200px; margin: auto; font-family: Courier; text-decoration: none;' href='{google_form_url}'>Enroll Now</a>
    """, unsafe_allow_html=True)

    # Copyright notice
    st.markdown("""
    <hr>
    <p style='text-align: center; font-family: Courier;'>All Rights Reserved <a href='http://www.habdulhaq.com' target='_blank'>www.habdulhaq.com</a> 2024</p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
