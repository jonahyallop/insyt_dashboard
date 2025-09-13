import streamlit as st
import streamlit_authenticator as stauth

# Define users - to be moved to .yaml or .env
names = ["Jonah", "Donnie"]
usernames = ["jonah", "donnie"]

# Hashing passwords for security
passwords = stauth.Hasher(["jy123", "df123"]).generate()

credentials = {
    "usernames": {
        usernames[i]: {
            "name": names[i],
            "password": passwords[i]
        } for i in range(len(usernames))
    }
}

# --- Authenticator instance ---
authenticator = stauth.Authenticate(
    credentials,
    "my_cookie_name",   # cookie name
    "my_signature_key", # key to encrypt the cookie
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

# --- Login logic ---
if authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
else:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name}!")
    
    # Now show your normal app
    st.title("Club Dashboard")
    st.write("Select an age group to explore:")

st.set_page_config(page_title="Club Dashboard", layout="wide")

st.title("Club Dashboard")

st.write("Select an age group to explore players:")

age_groups = ["Under 19s", "Under 17s", "Under 16s", "Under 15s", 
              "Under 14s", "Under 13s", "Under 12s"]

for group in age_groups:
    if st.button(group):
        st.session_state["selected_group"] = group
        st.switch_page("pages/1_Player_Dashboard.py")
