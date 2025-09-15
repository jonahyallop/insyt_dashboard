import streamlit as st
import pandas as pd
import os
import yaml
from yaml import SafeLoader

# --- Load configuration from YAML ---
with open("config/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

st.title("👥 Player Dashboard")

# Get club and group from session state
club = st.session_state.get("club")
group = st.session_state.get("selected_group")

# Load the player data for the users club
players = pd.read_csv(f"data/players_{club}")

st.subheader(f"Players in {group}")
group_players = players[players["age_group"] == group]

player = st.selectbox("Select a player:", group_players["name"].tolist())

if st.button("Go to Overview"):
    st.session_state["selected_player"] = player
    st.switch_page(os.path.join("pages/2_Player_Overview.py"))
