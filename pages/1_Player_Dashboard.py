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

# Load the player data for the user's club
players = pd.read_csv(f"data/players_{club}")

# Filter for this age group
group_players = players[players["age_group"] == group]

st.subheader(f"{group} Formation (4-2-3-1)")

# --- Pitch Styling ---
st.markdown(
    """
    <style>
    .pitch {
        background: #228B22;
        border: 3px solid white;
        border-radius: 8px;
        padding: 30px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Utility: display a player card ---
def player_card(player_row):
    if player_row is None:
        st.empty()
        return

    name = player_row["name"]
    # Example: pick one or two stats to show
    stat = f"Goals: {player_row.get('goals', 'N/A')} | Assists: {player_row.get('assists', 'N/A')}"
    
    if st.button(name, key=name):
        st.session_state["selected_player"] = name
        st.switch_page(os.path.join("pages/2_Player_Overview.py"))
    st.caption(stat)

# --- Map positions to players ---
positions = {
    "GK": None,
    "LB": None,
    "LCB": None,
    "RCB": None,
    "RB": None,
    "LDM": None,
    "RDM": None,
    "CAM": None,
    "LW": None,
    "RW": None,
    "ST": None,
}

for pos in positions.keys():
    match = group_players[group_players["position"] == pos]
    if not match.empty:
        positions[pos] = match.iloc[0]

# --- Formation Layout (4-2-3-1) ---
st.markdown('<div class="pitch">', unsafe_allow_html=True)

# Striker
cols = st.columns([2,1,2])
with cols[1]: player_card(positions["ST"])

# Attacking Midfield
cols = st.columns(3)
for key in ["LW", "CAM", "RW"]:
    with cols[["LW","CAM","RW"].index(key)]: player_card(positions[key])

# Defensive Midfield
cols = st.columns([1,1,1])
for key in ["CDM1", "CDM2"]:
    with cols[["CDM1","CDM2"].index(key)+1]: player_card(positions[key])

# Defense
cols = st.columns(4)
for key in ["LB", "CB1", "CB2", "RB"]:
    with cols[["LB","CB1","CB2","RB"].index(key)]: player_card(positions[key])

# Goalkeeper
cols = st.columns([2,1,2])
with cols[1]: player_card(positions["GK"])

st.markdown('</div>', unsafe_allow_html=True)
