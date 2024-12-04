import streamlit as st
import os
import json
import requests
import urllib.parse

# ------------------------------
# Auth0 Configuration
# ------------------------------
AUTH0_DOMAIN = 'dev-fe5xpi2tlu60xwyp.us.auth0.com'
AUTH0_CLIENT_ID = 'Frk7PWaSV0TpxBaOnmvbtjJSu0767TdX'
AUTH0_CLIENT_SECRET = st.secrets["auth0"]["AUTH0_CLIENT_SECRET"]  # Retrieved securely
AUTH0_CALLBACK_URL = 'https://manageyourenergy.streamlit.app/'  # Your app's URL
AUTH0_AUDIENCE = f'https://{AUTH0_DOMAIN}/userinfo'
AUTH0_AUTHORIZE_URL = f'https://{AUTH0_DOMAIN}/authorize'
AUTH0_TOKEN_URL = f'https://{AUTH0_DOMAIN}/oauth/token'
AUTH0_USER_INFO_URL = f'https://{AUTH0_DOMAIN}/userinfo'

# ------------------------------
# App Setup
# ------------------------------
st.set_page_config(page_title="Energy Log App", page_icon="⚡")
st.title("⚡ Energy Log App with Auth0 Authentication")

# Directory to store user data
USER_DATABASE = "database/users/"
if not os.path.exists(USER_DATABASE):
    os.makedirs(USER_DATABASE)

# Initialize session state variables
if "auth0_token" not in st.session_state:
    st.session_state["auth0_token"] = None
if "email" not in st.session_state:
    st.session_state["email"] = None

# ------------------------------
# Authentication Functions
# ------------------------------
def login():
    params = {
        'client_id': AUTH0_CLIENT_ID,
        'redirect_uri': AUTH0_CALLBACK_URL,
        'scope': 'openid profile email',
        'response_type': 'code',
        'audience': AUTH0_AUDIENCE,
    }
    auth_url = AUTH0_AUTHORIZE_URL + '?' + urllib.parse.urlencode(params)
    st.markdown(f"Please [log in]({auth_url}) to continue.")

def get_token(code):
    data = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': AUTH0_CALLBACK_URL,
    }
    response = requests.post(AUTH0_TOKEN_URL, data=data)
    response.raise_for_status()
    return response.json()

def get_user_info(token):
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(AUTH0_USER_INFO_URL, headers=headers)
    response.raise_for_status()
    return response.json()

# ------------------------------
# Data Handling Functions
# ------------------------------
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

# ------------------------------
# Main App Logic
# ------------------------------
query_params = st.query_params  # Updated function
if "code" in query_params:
    code = query_params["code"][0]
    try:
        token_info = get_token(code)
        st.session_state["auth0_token"] = token_info['access_token']
        user_info = get_user_info(st.session_state["auth0_token"])
        st.session_state["email"] = user_info['email']
        # Clear query parameters
        st.set_query_params()
        st.experimental_rerun()  # Update this line based on your Streamlit version
    except Exception as e:
        st.error(f"Authentication failed: {e}")
        st.stop()
elif st.session_state["auth0_token"]:
    # User is authenticated
    email = st.session_state["email"]
    st.sidebar.success(f"Signed in as {email}")

    # Main app functionality
    st.subheader(f"Welcome, {email}! Log Your Energy Levels Below.")
    data = load_user_data(email)

    # Log Energy Data
    st.write("## Log a New Entry")
    with st.form(key='entry_form'):
        time_block = st.selectbox(
            "Select Time Block",
            ["6–8 AM", "8–10 AM", "10–12 PM", "12–2 PM", "2–4 PM", "4–6 PM", "6–8 PM"]
        )
        energy_level = st.slider("Energy Level (1-10)", 1, 10, value=5)
        task = st.text_input("What task did you do?")
        notes = st.text_area("Additional Notes (optional)")
        submit = st.form_submit_button("Save Entry")
        if submit:
            data.append({
                "time_block": time_block,
                "energy_level": energy_level,
                "task": task,
                "notes": notes
            })
            save_user_data(email, data)
            st.success("Entry saved!")

    # Display Daily Entries
    st.write("## Your Daily Entries")
    if data:
        for entry in data:
            st.write(f"""
            **{entry['time_block']}**
            - Energy Level: {entry['energy_level']}/10
            - Task: {entry['task']}
            - Notes: {entry.get('notes', 'N/A')}
            """)
    else:
        st.write("No entries yet.")

    # Logout Button
    if st.sidebar.button("Log Out"):
        for key in ["auth0_token", "email"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()  # Update this line based on your Streamlit version
else:
    login()
    st.stop()
