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

# --- Map positions to coordinates (percentages) ---
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

# --- Render formation with HTML buttons ---
html = """
<style>
.pitch-container {
    position: relative;
    width: 100%;
    height: 600px;
    background-image: url('/Users/jonahyallop/Documents/04. Code Repositories/insyt_dashboard/images/Football Pitch Image.svg');
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
    background-color: rgba(0,0,0,0.5);
    color: white;
    border: 1px solid white;
    border-radius: 5px;
    cursor: pointer;
    padding: 2px 5px;
    font-size: 0.9rem;
    margin: 1px 0;
}
.player-btn:hover {
    background-color: gold;
    color: black;
}
</style>
<div class="pitch-container">
"""

# Add each position
for pos, players_list in positions.items():
    coords = position_coords.get(pos)
    top = coords["top"]
    left = coords["left"]
    html += f'<div class="position-box" style="top:{top}%; left:{left}%;">'
    html += f'<div><strong>{pos}</strong></div>'
    for i, p in enumerate(players_list[:3]):
        name = p["name"]
        html += f'<button class="player-btn" onclick="window.alert(\'Selected: {name}\')">{name}</button><br>'
    html += '</div>'

html += "</div>"

st.markdown(html, unsafe_allow_html=True)
