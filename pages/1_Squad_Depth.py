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

# --- CSS Styling ---
st.markdown(
    """
    <style>
    .pitch {
        position: relative;
        background: #228B22;
        border: 3px solid white;
        border-radius: 8px;
        padding: 40px;
        margin: auto;
        width: 90%;
        height: 600px; /* set height for half pitch */
    }

    /* Halfway line */
    .pitch::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 5%;
        width: 90%;
        height: 0;
        border-top: 2px solid white;
    }

    /* Penalty box */
    .penalty-box {
        position: absolute;
        bottom: 0;
        left: 25%;
        width: 50%;
        height: 20%;
        border: 2px solid white;
    }

    /* Goal box */
    .goal-box {
        position: absolute;
        bottom: 0;
        left: 40%;
        width: 20%;
        height: 10%;
        border: 2px solid white;
    }

    /* Centre circle */
    .centre-circle {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 15%;
        height: 15%;
        border: 2px solid white;
        border-radius: 50%;
        transform: translate(-50%, -50%);
    }

    /* Your existing styles */
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
    st.markdown(f"<div class='position-box'>{pos_label}</div>", unsafe_allow_html=True)
    # Up to 3 slots
    for i in range(3):
        if i < len(players):
            p = players[i]
            name = p["name"]
            if st.button(name, key=f"{pos_label}_{name}", help=f"Click to view {name}", use_container_width=True):
                st.session_state["selected_player"] = name
                st.switch_page(os.path.join("pages/2_Player_Information.py"))
        else:
            st.markdown("<div class='player-slot'>&nbsp;</div>", unsafe_allow_html=True)

# --- Formation Layout (rows) ---
st.markdown('<div class="pitch">', unsafe_allow_html=True)
st.markdown('<div class="penalty-box"></div>', unsafe_allow_html=True)
st.markdown('<div class="goal-box"></div>', unsafe_allow_html=True)
st.markdown('<div class="centre-circle"></div>', unsafe_allow_html=True)

# Striker
cols = st.columns([3,1,3])
with cols[1]:
    position_box("ST", positions["ST"])

# Attacking Midfield
cols = st.columns(3)
with cols[0]: position_box("LW", positions["LW"])
with cols[1]: position_box("CAM", positions["CAM"])
with cols[2]: position_box("RW", positions["RW"])

# Defensive Midfield
cols = st.columns([2,1,1,2])
with cols[1]: position_box("LDM", positions["LDM"])
with cols[2]: position_box("RDM", positions["RDM"])

# Defense
cols = st.columns(4)
with cols[0]: position_box("LB", positions["LB"])
with cols[1]: position_box("LCB", positions["LCB"])
with cols[2]: position_box("RCB", positions["RCB"])
with cols[3]: position_box("RB", positions["RB"])

# Goalkeeper
cols = st.columns([3,1,3])
with cols[1]:
    position_box("GK", positions["GK"])

st.markdown('</div>', unsafe_allow_html=True)
