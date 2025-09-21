import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Player Information", layout="wide")

# --- Title ---
st.title("Player Information")

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

# --- Header / Player summary ---
st.markdown(f"## {player}")
st.markdown(f"**Age:** {pinfo['age']} | **Position:** {pinfo['position']} | **Group:** {group}")

# --- Player details in 2 columns ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Basic Information")
    st.write(f"**DOB:** {pinfo['dob']}")
    st.write(f"**Height:** {pinfo['height']} cm")
    st.write(f"**Weight:** {pinfo['weight']} kg")

    st.subheader("👨‍👩‍👦 Family")
    st.write("Family info goes here…")

    st.subheader("🏫 School")
    st.write("School info goes here…")

with col2:
    st.subheader("⚽ Sports Background")
    st.write("Sports info goes here…")

    st.subheader("🩺 Medical")
    st.write("Medical info goes here…")

    st.subheader("📜 Declarations")
    st.write("Declarations info goes here…")

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

st.subheader(f"📈 Subjective Ratings: {player} vs {group} Average")
st.plotly_chart(fig, use_container_width=True)

# --- Objective Tests as metrics ---
st.subheader("⚡ Objective Tests")

mcol1, mcol2, mcol3, mcol4 = st.columns(4)
mcol1.metric("Speed 5m", f"{pdata['speed5m']}s")
mcol2.metric("Speed 10m", f"{pdata['speed10m']}s")
mcol3.metric("Speed 15m", f"{pdata['speed15m']}s")
mcol4.metric("Explosivity", f"{pdata['explosivity']}")
