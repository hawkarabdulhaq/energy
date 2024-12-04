import streamlit as st
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import os
import json
from google.auth.transport.requests import Request

# App setup
st.title("Energy Log App with Google Sign-In")

# Directory to store user data
USER_DATABASE = "database/users/"
os.makedirs(USER_DATABASE, exist_ok=True)

# Google OAuth Configurations
GOOGLE_CLIENT_ID = st.secrets["google_client_id"]
GOOGLE_CLIENT_SECRET = st.secrets["google_client_secret"]
REDIRECT_URI = st.secrets["redirect_uri"]

# OAuth flow
flow = Flow.from_client_config(
    {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI],
        }
    },
    scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],
)

# Authentication Functions
def get_user_email():
    """Authenticate user using Google Sign-In and return their email."""
    auth_url, state = flow.authorization_url(prompt="consent")
    st.write(f"[Click here to sign in with Google]({auth_url})")
    query_params = st.experimental_get_query_params()

    if "code" in query_params:
        code = query_params["code"][0]
        flow.fetch_token(code=code)
        credentials = flow.credentials
        id_info = id_token.verify_oauth2_token(credentials.id_token, Request(), GOOGLE_CLIENT_ID)
        return id_info.get("email")
    return None

def load_user_data(email):
    """Load the user's data from their JSON file."""
    user_file = os.path.join(USER_DATABASE, f"{email}.json")
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_data = json.load(file)
            return user_data.get("entries", [])
    return []

def save_user_data(email, data):
    """Save the user's data to their JSON file."""
    user_file = os.path.join(USER_DATABASE, f"{email}.json")
    user_data = {"entries": data}
    with open(user_file, "w") as file:
        json.dump(user_data, file)

# Main App Logic
email = get_user_email()
if email:
    st.sidebar.success(f"Signed in as {email}")
    st.subheader(f"Welcome, {email}! Log Your Energy Levels Below.")
    data = load_user_data(email)

    # Log Energy Data
    time_block = st.selectbox("Select Time Block", ["6–8 AM", "8–10 AM", "10–12 PM", "12–2 PM", "2–4 PM", "4–6 PM", "6–8 PM"])
    energy_level = st.slider("Energy Level (1-10)", 1, 10)
    task = st.text_input("What task did you do?")
    notes = st.text_area("Additional Notes (optional)")

    if st.button("Save Entry"):
        data.append({"time_block": time_block, "energy_level": energy_level, "task": task, "notes": notes})
        save_user_data(email, data)
        st.success("Entry saved!")

    # Display Daily Entries
    st.subheader("Your Daily Entries")
    for entry in data:
        st.write(f"**{entry['time_block']}**: Energy {entry['energy_level']}/10 | Task: {entry['task']} | Notes: {entry.get('notes', 'N/A')}")
else:
    st.warning("Please sign in to continue.")
