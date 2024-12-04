import streamlit as st
import os
import json
import requests
import urllib.parse

# Auth0 Configuration
AUTH0_DOMAIN = 'YOUR_AUTH0_DOMAIN'  # e.g., 'dev-abc123.us.auth0.com'
AUTH0_CLIENT_ID = 'YOUR_AUTH0_CLIENT_ID'
AUTH0_CLIENT_SECRET = 'YOUR_AUTH0_CLIENT_SECRET'
AUTH0_CALLBACK_URL = 'http://localhost:8501'  # Update with your callback URL
AUTH0_AUDIENCE = f'https://{AUTH0_DOMAIN}/userinfo'
AUTH0_AUTHORIZE_URL = f'https://{AUTH0_DOMAIN}/authorize'
AUTH0_TOKEN_URL = f'https://{AUTH0_DOMAIN}/oauth/token'
AUTH0_USER_INFO_URL = f'https://{AUTH0_DOMAIN}/userinfo'

# App setup
st.title("Energy Log App with Auth0 Authentication")

# Directory to store user data
USER_DATABASE = "database/users/"
if not os.path.exists(USER_DATABASE):
    os.makedirs(USER_DATABASE)

# Initialize session state variables
if "auth0_token" not in st.session_state:
    st.session_state["auth0_token"] = None
if "email" not in st.session_state:
    st.session_state["email"] = None

def login():
    params = {
        'client_id': AUTH0_CLIENT_ID,
        'redirect_uri': AUTH0_CALLBACK_URL,
        'scope': 'openid profile email',
        'response_type': 'code',
        'audience': AUTH0_AUDIENCE,
    }
    auth_url = AUTH0_AUTHORIZE_URL + '?' + urllib.parse.urlencode(params)
    st.write(f"[Click here to log in]({auth_url})")

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

# Main app logic
query_params = st.experimental_get_query_params()
if "code" in query_params:
    code = query_params["code"][0]
    token_info = get_token(code)
    st.session_state["auth0_token"] = token_info['access_token']
    user_info = get_user_info(st.session_state["auth0_token"])
    st.session_state["email"] = user_info['email']
    # Clear query parameters
    st.experimental_set_query_params()
    st.experimental_rerun()
elif st.session_state["auth0_token"]:
    # User is authenticated
    email = st.session_state["email"]
    st.sidebar.success(f"Signed in as {email}")

    # Your existing code to log energy levels
    # ...

    # Logout Button
    if st.sidebar.button("Log Out"):
        for key in ["auth0_token", "email"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()
else:
    login()
    st.stop()
