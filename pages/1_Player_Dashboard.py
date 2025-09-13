import streamlit as st
import pandas as pd
import os

st.title("👥 Player Dashboard")

players = pd.read_csv("data/players.csv")
group = st.session_state.get("selected_group", "Under 19s")

st.subheader(f"Players in {group}")
group_players = players[players["age_group"] == group]

player = st.selectbox("Select a player:", group_players["name"].tolist())

if st.button("Go to Overview"):
    st.session_state["selected_player"] = player
    st.switch_page(os.path.join("pages/2_Player_Overview.py"))
