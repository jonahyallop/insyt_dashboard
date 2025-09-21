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
players = pd.read_csv(f"data/players_{club}.csv")

# Filter for this age group
group_players = players[players["age_group"] == group]

st.subheader(f"Formation (4-2-3-1) — {group}")

# --- Map positions to players (lists, not single rows) ---
positions = {pos: [] for pos in [
    "GK", "LB", "LCB", "RCB", "RB", "LDM", "RDM", "CAM", "LW", "RW", "ST"
]}

for pos in positions.keys():
    matches = group_players[group_players["position"] == pos]
    if not matches.empty:
        positions[pos] = matches.to_dict("records")  # keep as list of dicts

# --- Styles: pitch + player buttons ---
PITCH_HEIGHT = 520

st.markdown(
    f"""
    <style>
    .formation-pitch {{
        background: #228B22;
        border: 3px solid white;
        border-radius: 10px;
        height: {PITCH_HEIGHT}px;
        margin: 12px 0 -{PITCH_HEIGHT - 40}px;
        position: relative;
        z-index: 0;
        pointer-events: none;
    }}

    div.stButton > button {{
        width: 140px !important;   /* fixed button width */
        height: 40px !important;   /* fixed button height */
        overflow: hidden !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;  /* truncate with … if too long */
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }}

    .player-stat {{
        font-size: 13px;
        color: rgba(255,255,255,0.9);
        margin-top: 6px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Green background block
st.markdown('<div class="formation-pitch"></div>', unsafe_allow_html=True)

# --- Utility: display a player card ---
def player_card(player_list, pos_label=None):
    if not player_list:
        st.empty()
        return

    # Show the position label once, centered above the stack
    if pos_label:
        st.markdown(
            f"<div style='text-align:center; font-weight:bold; color:white;'>{pos_label}</div>",
            unsafe_allow_html=True
        )

    # Show each player as a button + stat
    for player_row in player_list:
        name = player_row["name"]

        if st.button(name, key=f"{pos_label}_{name}"):
            st.session_state["selected_player"] = name
            st.switch_page(os.path.join("pages/2_Player_Overview.py"))


# --- Layout (9-column grid so ST, CAM, GK align) ---
# indices: 0..8, center = 4
# LB/LW = col 1, LCB/LDM = col 3, CAM/ST/GK = col 4, RDM/RCB = col 5, RW/RB = col 7

# Striker
cols = st.columns([3,1,3])
with cols[1]:
    player_card(positions["ST"], "ST")

# Attacking Midfield
cols = st.columns(3)
with cols[0]: player_card(positions["LW"], "LW")
with cols[1]: player_card(positions["CAM"], "CAM")
with cols[2]: player_card(positions["RW"], "RW")

# Defensive Midfield
cols = st.columns([2,1,1,2])
with cols[1]: player_card(positions["LDM"], "LDM")
with cols[2]: player_card(positions["RDM"], "RDM")

# Defense
cols = st.columns(4)
with cols[0]: player_card(positions["LB"], "LB")
with cols[1]: player_card(positions["LCB"], "LCB")
with cols[2]: player_card(positions["RCB"], "RCB")
with cols[3]: player_card(positions["RB"], "RB")

# Goalkeeper
cols = st.columns([3,1,3])
with cols[1]:
    player_card(positions["GK"], "GK")
