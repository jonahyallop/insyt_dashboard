# formation_page.py  (replace your existing file content with this)
import streamlit as st
import pandas as pd
import base64
import yaml
from yaml import SafeLoader
import urllib.parse
import html as html_lib
import streamlit.components.v1 as components
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

# --- Clean map positions to coordinates (unique & sensible values) ---
position_coords = {
    "GK":  {"top": 95, "left": 50},
    "LB":  {"top": 75, "left": 20},
    "LCB": {"top": 75, "left": 35},
    "RCB": {"top": 75, "left": 65},
    "RB":  {"top": 75, "left": 80},
    "LDM": {"top": 55, "left": 42},
    "RDM": {"top": 55, "left": 58},
    "LW":  {"top": 35, "left": 25},
    "CAM": {"top": 35, "left": 50},
    "RW":  {"top": 35, "left": 75},
    "ST":  {"top": 15, "left": 50},
}

# --- Build positions dict in the order we want to show them ---
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

# --- Encode local image to Base64 (use PNG or SVG) ---
image_path = "images/Football Pitch Image.svg"  # adjust path if needed
with open(image_path, "rb") as f:
    image_bytes = f.read()
    b64_image = base64.b64encode(image_bytes).decode()

# --- Build the full HTML (single chunk) to render in a component iframe ---
# Adjust the CSS height here (and the components.html height below) if you want larger/smaller
container_height_px = 900

html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <style>
    html,body {{
      margin: 0;
      padding: 0;
      height: 100%;
      background: transparent;
    }}
    .pitch-container {{
      position: relative;
      width: 100%;
      height: {container_height_px}px;
      background-image: url("data:image/svg+xml;base64,{b64_image}");
      background-size: contain;
      background-repeat: no-repeat;
      background-position: center bottom;
      overflow: hidden;
    }}
    .position-box {{
      position: absolute;
      transform: translate(-50%, -50%);
      text-align: center;
      pointer-events: auto;
    }}
    /* style anchor to look like a button */
    .player-btn {{
      display: inline-block;
      background-color: rgba(0,0,0,0.65);
      color: #fff;
      border: 1px solid #fff;
      border-radius: 6px;
      padding: 4px 8px;
      margin: 2px 0;
      text-decoration: none;
      font-weight: 600;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      font-size: 0.9rem;
      cursor: pointer;
    }}
    .player-btn:hover {{
      background-color: gold;
      color: black;
    }}
    .pos-label {{
      color: white;
      font-weight: 700;
      margin-bottom: 4px;
      text-shadow: 0 0 4px rgba(0,0,0,0.8);
    }}
  </style>
</head>
<body>
  <div class="pitch-container">
"""

# Add each position and players inside it
for pos, players_list in positions.items():
    coords = position_coords.get(pos)
    if not coords:
        continue
    top = coords["top"]
    left = coords["left"]

    # Open position box
    html += f'<div class="position-box" style="top:{top}%; left:{left}%;">'
    html += f'<div class="pos-label">{html_lib.escape(pos)}</div>'

    # Add up to 3 players (you can change number)
    for p in players_list[:3]:
        name = p["name"]
        label = html_lib.escape(name)
        url_name = urllib.parse.quote_plus(name)  # safe for URL param
        # anchor sets target to parent frame so it changes the top-level Streamlit URL
        html += f'<a class="player-btn" href="?selected_player={url_name}" target="_parent">{label}</a><br/>'

    html += '</div>'

# Close container and body
html += """
  </div>
</body>
</html>
"""

# --- Render the HTML iframe component ---
components.html(html, height=container_height_px, scrolling=False)

# --- After the component is shown, handle navigation in Streamlit based on query param ---
params = st.experimental_get_query_params()
# --- After the component is shown, handle navigation in Streamlit based on query param ---
if "selected_player" in st.query_params:
    selected_player = st.query_params["selected_player"]
    st.session_state["selected_player"] = selected_player

    # (Optional) clear query param so page reloads cleanly after redirect
    st.query_params.clear()

    # Navigate to the player info page
    st.switch_page("pages/2_Player_Information.py")
