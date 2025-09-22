import streamlit as st
import pandas as pd
import os
import yaml
from yaml import SafeLoader

# --- Load configuration from YAML ---
with open("config/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Get club and group from session state
club = st.session_state.get("club")
group = st.session_state.get("selected_group")

st.title(f"{group} Squad Depth")

# Load the player data for the user's club
players = pd.read_csv(f"data/players_{club}.csv")

# Filter for this age group
group_players = players[players["age_group"] == group]

st.subheader("Formation (4-2-3-1)")

# --- CSS Styling (background pitch + controls) ---
st.markdown(
    """
    <style>
    .pitch {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/4/45/Football_field.svg");
        background-size: contain;
        background-repeat: no-repeat; 
        background-position: center center;
        background-color: #228B22; /* fallback green */
        border: 3px solid white;
        border-radius: 8px;
        padding: 40px;
        margin: auto;
        min-height: 600px;
    }
    .position-box {
        border: 2px solid white;
        border-radius: 6px;
        padding: 6px;
        margin: 4px;
        background-color: rgba(255,255,255,0.1);
        text-align: center;
        color: white;
        font-weight: bold;
    }
    .player-slot {
        margin: 4px 0;
    }
    .player-btn {
        background: none;
        border: none;
        color: #fff;
        text-decoration: underline;
        cursor: pointer;
        font-size: 0.9rem;
    }
    .player-btn:hover {
        color: #FFD700; /* gold highlight */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Build position map ---
position_order = [
    ["ST"],
    ["LW", "CAM", "RW"],
    ["LDM", "RDM"],
    ["LB", "LCB", "RCB", "RB"],
    ["GK"]
]

positions = {pos: [] for row in position_order for pos in row}

for pos in positions.keys():
    matches = group_players[group_players["position"] == pos]
    if not matches.empty:
        positions[pos] = matches.to_dict(orient="records")

# --- Utility: render a position box ---
def position_box(pos_label, players):
    # show the position header (HTML)
    st.markdown(f"<div class='position-box'>{pos_label}</div>", unsafe_allow_html=True)
    # Up to 3 player buttons per position (change to desired number)
    for i in range(3):
        if i < len(players):
            p = players[i]
            name = p["name"]
            # Streamlit button for interactivity (this will render above the background)
            if st.button(name, key=f"{pos_label}_{name}", help=f"Click to view {name}", use_container_width=True):
                st.session_state["selected_player"] = name
                # change path to your player info page
                st.switch_page(os.path.join("pages/2_Player_Information.py"))
        else:
            # empty slot - small spacing so layout stays consistent
            st.markdown("<div class='player-slot'>&nbsp;</div>", unsafe_allow_html=True)

# --- Formation Layout inside a visible frame ---
st.markdown('<div class="pitch-frame">', unsafe_allow_html=True)

# Striker (centered)
cols = st.columns([3,1,3])
with cols[1]:
    position_box("ST", positions["ST"])

# Attacking Midfield (3 across)
cols = st.columns(3)
with cols[0]: position_box("LW", positions["LW"])
with cols[1]: position_box("CAM", positions["CAM"])
with cols[2]: position_box("RW", positions["RW"])

# Defensive Midfield (2 in centre)
cols = st.columns([2,1,1,2])
with cols[1]: position_box("LDM", positions["LDM"])
with cols[2]: position_box("RDM", positions["RDM"])

# Defense (4 across)
cols = st.columns(4)
with cols[0]: position_box("LB", positions["LB"])
with cols[1]: position_box("LCB", positions["LCB"])
with cols[2]: position_box("RCB", positions["RCB"])
with cols[3]: position_box("RB", positions["RB"])

# Goalkeeper (centered)
cols = st.columns([3,1,3])
with cols[1]:
    position_box("GK", positions["GK"])

st.markdown('</div>', unsafe_allow_html=True)
