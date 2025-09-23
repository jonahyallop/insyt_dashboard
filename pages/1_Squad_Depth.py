# formation_page.py
import streamlit as st
import pandas as pd
import base64
import yaml
from yaml import SafeLoader
import html as html_lib
import streamlit.components.v1 as components

# --- Load configuration ---
with open("config/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

club = st.session_state.get("club")
group = st.session_state.get("selected_group")

st.title(f"{group} Squad Depth")

players = pd.read_csv(f"data/players_{club}.csv")
group_players = players[players["age_group"] == group]

st.subheader("Formation (4-2-3-1)")

# --- Map positions to coordinates ---
position_coords = {
    "GK":  {"top": 89, "left": 50},
    "LB":  {"top": 65, "left": 28},
    "LCB": {"top": 75, "left": 40},
    "RCB": {"top": 75, "left": 60},
    "RB":  {"top": 65, "left": 72},
    "LDM": {"top": 52, "left": 42},
    "RDM": {"top": 52, "left": 58},
    "LW":  {"top": 35, "left": 30},
    "CAM": {"top": 35, "left": 50},
    "RW":  {"top": 35, "left": 70},
    "ST":  {"top": 15, "left": 50},
}

# --- Order of positions ---
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

# --- Load pitch image ---
image_path = "images/Football Pitch Image.svg"
with open(image_path, "rb") as f:
    image_bytes = f.read()
    b64_image = base64.b64encode(image_bytes).decode()

# --- Build HTML ---
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
      background-color: white;
      border: 2px solid black;
      border-radius: 6px;
      padding: 4px;
      min-width: 180px;
      max-width: 220px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      font-size: 0.75rem;
      overflow-x: auto;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    th, td {{
      border: 1px solid black;
      padding: 2px 4px;
      text-align: center;
      font-size: 0.7rem;
    }}
    th {{
      background-color: #f0f0f0;
      font-weight: 700;
    }}
  </style>
</head>
<body>
  <div class="pitch-container">
"""

# Add each position table
for pos, players_list in positions.items():
    coords = position_coords.get(pos)
    if not coords:
        continue
    top = coords["top"]
    left = coords["left"]

    html += f'<div class="position-box" style="top:{top}%; left:{left}%;">'

    # Table header
    html += """
    <table>
      <tr>
        <th>Name</th>
        <th>Age</th>
        <th>Bio. Age</th>
        <th>Status</th>
      </tr>
    """

    # Up to 3 players
    for p in players_list[:3]:
        name = html_lib.escape(p.get("name", ""))
        age = p.get("age", "")
        bio_age = p.get("bio_age", "")
        status = html_lib.escape(p.get("maturation_status", ""))
        html += f"""
          <tr>
            <td>{name}</td>
            <td>{age}</td>
            <td>{bio_age}</td>
            <td>{status}</td>
          </tr>
        """

    html += "</table></div>"

html += """
  </div>
</body>
</html>
"""

# --- Render ---
components.html(html, height=container_height_px, scrolling=False)
