import streamlit as st
import pandas as pd
import base64
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

# --- Map positions to coordinates (percentages) for taller half-pitch ---
position_coords = {
    "GK": {"top": 95, "left": 50},
    "LB": {"top": 75, "left": 12},
    "LCB": {"top": 75, "left": 35},
    "RCB": {"top": 75, "left": 65},
    "RB": {"top": 75, "left": 88},
    "LDM": {"top": 55, "left": 42},
    "RDM": {"top": 55, "left": 58},
    "LW": {"top": 35, "left": 18},
    "CAM": {"top": 35, "left": 50},
    "RW": {"top": 35, "left": 82},
    "ST": {"top": 15, "left": 50},
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

# --- Encode local image to Base64 ---
image_path = "images/Football Pitch Image.svg"  # make sure this path is correct
with open(image_path, "rb") as f:
    image_bytes = f.read()
    b64_image = base64.b64encode(image_bytes).decode()

# --- Render formation with HTML buttons using Base64 image ---
html = f"""
<style>
.pitch-container {{
    position: relative;
    width: 100%;
    aspect-ratio: 2/1;  /* maintain width:height ratio */
    background-image: url("data:image/png;base64,{b64_image}");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center bottom;
    margin: auto;
}}
.position-box {{
    position: absolute;
    transform: translate(-50%, -50%);
    text-align: center;
}}
.player-btn {{
    background-color: rgba(0,0,0,0.5);
    color: white;
    border: 1px solid white;
    border-radius: 5px;
    cursor: pointer;
    padding: 2px 5px;
    font-size: 0.9rem;
    margin: 1px 0;
}}
.player-btn:hover {{
    background-color: gold;
    color: black;
}}
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
