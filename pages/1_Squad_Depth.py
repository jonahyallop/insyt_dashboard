import streamlit as st
import pandas as pd
import base64
import yaml
from yaml import SafeLoader
import os

# --- Load configuration ---
with open("config/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

club = st.session_state.get("club")
group = st.session_state.get("selected_group")

st.title(f"{group} Squad Depth")

players = pd.read_csv(f"data/players_{club}.csv")
group_players = players[players["age_group"] == group]

st.subheader("Formation (4-2-3-1)")

# --- Map positions to coordinates for taller half-pitch ---
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
image_path = "images/Football Pitch Image.svg"  # use PNG or SVG
with open(image_path, "rb") as f:
    image_bytes = f.read()
    b64_image = base64.b64encode(image_bytes).decode()

# --- CSS for background pitch and player buttons ---
st.markdown(f"""
<style>
.pitch-container {{
    position: relative;
    width: 100%;
    height: 900px;  /* fixed height ensures the image shows correctly */
    background-image: url("data:image/png;base64,{b64_image}");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center bottom; /* goal at bottom */
    margin: auto;
}}
.position-box {{
    position: absolute;
    transform: translate(-50%, -50%);
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
</style>
""", unsafe_allow_html=True)

# --- Render the pitch container ---
st.markdown('<div class="pitch-container">', unsafe_allow_html=True)

# Use columns with relative width to position Streamlit buttons
for pos, players_list in positions.items():
    coords = position_coords.get(pos)
    top_pct = coords["top"]
    left_pct = coords["left"]

    # Use a container div for absolute positioning
    st.markdown(f'<div class="position-box" style="top:{top_pct}%; left:{left_pct}%;">', unsafe_allow_html=True)

    st.markdown(f"<strong>{pos}</strong>", unsafe_allow_html=True)

    # Render up to 3 Streamlit buttons per position
    for i, p in enumerate(players_list[:3]):
        name = p["name"]
        if st.button(name, key=f"{pos}_{name}", use_container_width=True):
            st.session_state["selected_player"] = name
            st.switch_page(os.path.join("pages/2_Player_Information.py"))

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
