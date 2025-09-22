import streamlit as st
import pandas as pd
import os
import yaml
from yaml import SafeLoader

# --- Load configuration ---
with open("config/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

club = st.session_state.get("club")
group = st.session_state.get("selected_group")

st.title(f"{group} Squad Depth")

players = pd.read_csv(f"data/players_{club}.csv")
group_players = players[players["age_group"] == group]

st.subheader("Formation (4-2-3-1)")

# --- CSS for pitch and overlay ---
st.markdown(
    """
    <style>
    .pitch-container {
        position: relative;
        width: 100%;
        height: 600px;
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/4/45/Football_field.svg");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center center;
        margin: auto;
    }
    .position-box {
        position: absolute;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    .player-btn {
        margin: 2px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Map positions to coordinates (percent) ---
position_coords = {
    "GK": {"top": 92, "left": 50},
    "LB": {"top": 70, "left": 12},
    "LCB": {"top": 70, "left": 35},
    "RCB": {"top": 70, "left": 65},
    "RB": {"top": 70, "left": 88},
    "LDM": {"top": 50, "left": 42},
    "RDM": {"top": 50, "left": 58},
    "LW": {"top": 30, "left": 18},
    "CAM": {"top": 30, "left": 50},
    "RW": {"top": 30, "left": 82},
    "ST": {"top": 10, "left": 50},
}

# --- Build positions dict ---
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

# --- Utility to render position box with Streamlit buttons ---
def render_position(pos_label, players_list):
    coords = position_coords.get(pos_label, {"top": 0, "left": 0})
    top = coords["top"]
    left = coords["left"]

    st.markdown(f'<div class="position-box" style="top:{top}%; left:{left}%;">', unsafe_allow_html=True)

    st.markdown(f"<strong>{pos_label}</strong><br>", unsafe_allow_html=True)
    for i, p in enumerate(players_list[:3]):
        name = p["name"]
        if st.button(name, key=f"{pos_label}_{name}", use_container_width=True):
            st.session_state["selected_player"] = name
            st.switch_page(os.path.join("pages/2_Player_Information.py"))
    st.markdown("</div>", unsafe_allow_html=True)

# --- Render pitch ---
st.markdown('<div class="pitch-container">', unsafe_allow_html=True)

for pos, players_list in positions.items():
    render_position(pos, players_list)

st.markdown('</div>', unsafe_allow_html=True)
