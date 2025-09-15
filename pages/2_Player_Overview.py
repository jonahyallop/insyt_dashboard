import streamlit as st
import pandas as pd

st.title("📊 Player Overview")

player = st.session_state.get("selected_player", None)
if not player:
    st.warning("Go back and select a player first.")
    st.stop()

# Get user's club from session state
club = st.session_state.get("club")

# Load the player data for the users club
players = pd.read_csv(f"data/players_{club}")

pinfo = players[players["name"] == player].iloc[0]

st.subheader(player)
st.write(f"**Age:** {pinfo['age']} | **Position:** {pinfo['position']}")

tabs = st.tabs(["Basic", "Family", "School", "Sports", "Medical", "Declarations"])

with tabs[0]:
    st.write(f"**DOB:** {pinfo['dob']}")
    st.write(f"**Height:** {pinfo['height']} cm")
    st.write(f"**Weight:** {pinfo['weight']} kg")

with tabs[1]:
    st.write("Family info goes here…")
