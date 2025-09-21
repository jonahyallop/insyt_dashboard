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

        # Get the club of the user
        username = st.session_state["username"]
        club = config['credentials']['usernames'][username]['club']
        st.session_state["club"] = club

        # Add heading
        st.subheader("Select an age group to see detailed player information.")

        # Add logout button in sidebar
        authenticator.logout("Logout", location="sidebar")

        st.set_page_config(page_title="Club Dashboard", layout="wide")

        # Define age groups - 
        age_groups = ["Under 12s", "Under 13s", "Under 14s", "Under 15s", 
        "Under 16s", "Under 17s", "Under 19s"]

        # Add dropdown for user to select age group
        selected_group = st.selectbox("Select an age group", age_groups)

        if st.button("Go"):
            st.session_state["selected_group"] = selected_group
            st.switch_page("pages/2_Squad_Depth.py")

    elif st.session_state["authentication_status"] is False:
        # Wrong credentials
        st.error("Username/password is incorrect")

    elif st.session_state["authentication_status"] is None:
        # User hasn’t attempted login yet
        st.warning("Please log in to access the dashboard")
    else:
        # Authentication status not set yet
        st.warning("Please log in to access the dashboard")