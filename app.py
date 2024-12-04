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
AUTH0_AUDIENCE = 'https://dev-fe5xpi2tlu60xwyp.us.auth0.com/api/v2/'  # Updated API Identifier
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
    st.write("Debug: Login URL", auth_url)  # Log the login URL for debugging
    st.markdown(f"Please [log in]({auth_url}) to continue.")

def get_token(code):
    data = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': AUTH0_CALLBACK_URL,
    }
    st.write("Debug: Token request payload", data)  # Log the data sent to Auth0
    response = requests.post(AUTH0_TOKEN_URL, data=data)
    st.write("Debug: Token response status code", response.status_code)  # Log response status
    st.write("Debug: Token response content", response.text)  # Log response content
    response.raise_for_status()  # Raise exception if there's an error
    return response.json()

def get_user_info(token):
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(AUTH0_USER_INFO_URL, headers=headers)
    response.raise_for_status()
    return response.json()

# ------------------------------
# Main App Logic
# ------------------------------
query_params = st.query_params
st.write("Debug: Raw query parameters", query_params)  # Log the raw query parameters

if "code" in query_params:
    code = query_params["code"][0].strip()  # Extract the full authorization code
    st.write("Debug: Extracted authorization code", code)  # Log the extracted code

    try:
        token_info = get_token(code)
        st.session_state["auth0_token"] = token_info['access_token']
        st.write("Debug: Token info", token_info)  # Log token info
        user_info = get_user_info(st.session_state["auth0_token"])
        st.session_state["email"] = user_info['email']
        st.write("Debug: User info", user_info)  # Log user info
        st.set_query_params()  # Clear query params
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Authentication failed: {e}")
        st.stop()

elif st.session_state["auth0_token"]:
    email = st.session_state["email"]
    st.sidebar.success(f"Signed in as {email}")
else:
    login()
    st.stop()
