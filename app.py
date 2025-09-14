import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- Load configuration from YAML ---
with open("config/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- Authenticator instance ---
authenticator = stauth.Authenticate(
    config['credentials'],
    "my_cookie_name",   # cookie name
    "my_signature_key", # key to encrypt the cookie
    cookie_expiry_days=30
)

# --- Display login widget ---
authenticator.login(location="main")

# --- Protect the dashboard content ---
if "authentication_status" in st.session_state:
    if st.session_state["authentication_status"]:
        # User is authenticated
        st.write(f"Welcome *{st.session_state['name']}*!")
        
        # Dashboard content starts here
        st.title("Football Dashboard")

        # Example: sidebar logout
        authenticator.logout("Logout", location="sidebar")
    
        st.set_page_config(page_title="Club Dashboard", layout="wide")

        age_groups = ["Under 19s", "Under 17s", "Under 16s", "Under 15s", 
                    "Under 14s", "Under 13s", "Under 12s"]

        for group in age_groups:
            if st.button(group):
                st.session_state["selected_group"] = group
                st.switch_page("pages/1_Player_Dashboard.py")

    elif st.session_state["authentication_status"] is False:
        # Wrong credentials
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        # User hasn’t attempted login yet
        st.warning("Please log in to access the dashboard")
else:
    # Authentication status not set yet
    st.warning("Please log in to access the dashboard")
