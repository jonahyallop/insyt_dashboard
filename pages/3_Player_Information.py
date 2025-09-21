import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Player Information", layout="wide")

# --- CSS for "cards" ---
st.markdown("""
    <style>
    .card {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .card h4 {
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("🏟️ Player Information")

# --- Get selected player ---
player = st.session_state.get("selected_player", None)
if not player:
    st.warning("Go back and select a player first.")
    st.stop()

# --- Get user's club ---
club = st.session_state.get("club")

# --- Load data ---
players = pd.read_csv(f"data/players_{club}.csv")
assessments = pd.read_csv(f"data/assessments_{club}.csv")

# --- Player info ---
pinfo = players[players["name"] == player].iloc[0]
pdata = assessments[assessments["name"] == player].iloc[0]
group = pinfo["age_group"]

# --- Header card ---
st.markdown(f"""
<div class="card">
    <h2>{player}</h2>
    <p><b>Age:</b> {pinfo['age']} &nbsp; | &nbsp; <b>Position:</b> {pinfo['position']} &nbsp; | &nbsp; <b>Group:</b> {group}</p>
</div>
""", unsafe_allow_html=True)

# --- Top row: basic info + background ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📌 Basic Info")
    st.write(f"**DOB:** {pinfo['dob']}")
    st.write(f"**Height:** {pinfo['height']} cm")
    st.write(f"**Weight:** {pinfo['weight']} kg")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 👨‍👩‍👦 Family")
    st.write("Family info goes here…")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🏫 School")
    st.write("School info goes here…")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### ⚽ Sports")
    st.write("Sports info goes here…")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🩺 Medical")
    st.write("Medical info goes here…")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Subjective Ratings Radar Chart ---
ratings = ["Receiving","Carrying","Distributing","Intelligence","Attitude","Learning"]

player_df = pd.DataFrame({
    "Skill": ratings,
    "Score": [pdata[r] for r in ratings],
    "Type": [player] * len(ratings)
})

group_players = players[players['age_group'] == group]['name'].tolist()
group_df = assessments[assessments["name"].isin(group_players)]
squad_avg = group_df[ratings].mean()

squad_df = pd.DataFrame({
    "Skill": ratings,
    "Score": squad_avg.values,
    "Type": [f"{group} Average"] * len(ratings)
})

radar_df = pd.concat([player_df, squad_df])

fig = px.line_polar(
    radar_df,
    r="Score",
    theta="Skill",
    color="Type",
    line_close=True,
    range_r=[0, 5]
)
fig.update_traces(fill="toself")

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f"#### 📈 Subjective Ratings: {player} vs {group} Avg")
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Objective Tests ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### ⚡ Objective Tests")

mcol1, mcol2, mcol3, mcol4 = st.columns(4)
mcol1.metric("Speed 5m", f"{pdata['speed5m']}s")
mcol2.metric("Speed 10m", f"{pdata['speed10m']}s")
mcol3.metric("Speed 15m", f"{pdata['speed15m']}s")
mcol4.metric("Explosivity", f"{pdata['explosivity']}")
st.markdown('</div>', unsafe_allow_html=True)
