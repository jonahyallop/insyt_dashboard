import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Player Assessment")

# Get selected player
player = st.session_state.get("selected_player", None)
if not player:
    st.warning("Go back and select a player first.")
    st.stop()

# Get user's club from session state
club = st.session_state.get("club")

# Load player data
players = pd.read_csv(f"data/players_{club}.csv")
assessments = pd.read_csv(f"data/assessments_{club}.csv")

# Player row
pdata = assessments[assessments["name"] == player].iloc[0]
group = players.loc[players["name"] == player, "age_group"].iloc[0]

# Subjective ratings
ratings = ["Receiving","Carrying","Distributing","Intelligence","Attitude","Learning"]

# Dataframe for player
player_df = pd.DataFrame({
    "Skill": ratings,
    "Score": [pdata[r] for r in ratings],
    "Type": [player] * len(ratings)
})

# Squad average for same age group
group_players = players[players['age_group'] == group]['name'].tolist()
group_df = assessments[assessments["name"].isin(group_players)]

squad_avg = group_df[ratings].mean()
squad_df = pd.DataFrame({
    "Skill": ratings,
    "Score": squad_avg.values,
    "Type": [f"{group} Average"] * len(ratings)
})

# Combine data
radar_df = pd.concat([player_df, squad_df])

# Plotly radar chart
fig = px.line_polar(radar_df,
                    r="Score",
                    theta="Skill",
                    color="Type",
                    line_close=True,
                    range_r=[0,5])

fig.update_traces(fill="toself")
st.subheader(f"Subjective Ratings: {player} vs {group} average")
st.plotly_chart(fig)

st.subheader("Objective Tests")
st.write(f"**Speed 5m:** {pdata['speed5m']}s")
st.write(f"**Speed 10m:** {pdata['speed10m']}s")
st.write(f"**Speed 15m:** {pdata['speed15m']}s")
st.write(f"**Explosivity:** {pdata['explosivity']}")