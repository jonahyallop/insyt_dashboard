import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Player Information", layout="wide")

# --- CSS for compact dashboard cards ---
st.markdown("""
    <style>
    .card {
        background-color: #1e1e1e;  /* dark mode friendly */
        padding: 0.8rem 1rem;
        border-radius: 0.5rem;
        border: 1px solid #333;
        margin-bottom: 1rem;
    }
    .card h2, .card h3, .card h4 {
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    .card p {
        margin: 0.2rem 0;
    }
    </style>
""", unsafe_allow_html=True)


club = st.session_state.get("club")

# --- Load players for chosen club ---
players = pd.read_csv(f"data/players_{club}.csv")
assessments = pd.read_csv(f"data/assessments_{club}.csv")

# Adding a page header
st.subheader("Player sashboard: select squad and player")

# --- Dropdowns for age group and player ---
age_groups = sorted(players["age_group"].unique())
age_group = st.selectbox("Select an Age Group", age_groups)

# Only players in the chosen age group
group_players_df = players[players["age_group"] == age_group]
group_players = group_players_df["name"].tolist()

player = st.selectbox("Select a Player", group_players)

# --- Once both selected, show dashboard ---
if player:
    # --- Player info ---
    pinfo = players[players["name"] == player].iloc[0]
    pdata = assessments[assessments["name"] == player].iloc[0]
    group = pinfo["age_group"]

    # --- Page title: Player name ---
    st.subheader(player)

    # --- Player Info Row (3 columns) ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <h4>📌 Player Info</h4>
            <p><b>Age:</b> {pinfo['age']}</p>
            <p><b>Position:</b> {pinfo['position']}</p>
            <p><b>Group:</b> {group}</p>
            <hr>
            <p><b>DOB:</b> {pinfo['dob']}</p>
            <p><b>Height:</b> {pinfo['height']} cm</p>
            <p><b>Weight:</b> {pinfo['weight']} kg</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <h4>👨‍👩‍👦 Family</h4>
            <p>Family info goes here…</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h4>🏫 School</h4>
            <p>School info goes here…</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <h4>⚽ Sports</h4>
            <p>Sports info goes here…</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h4>🩺 Medical</h4>
            <p>Medical info goes here…</p>
        </div>
        """, unsafe_allow_html=True)

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

    st.markdown(f"""
    <div class="card">
        <h4>📈 Subjective Ratings: {player} vs {group} Avg</h4>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

    # --- Objective Tests ---
    st.markdown(f"""
    <div class="card">
        <h4>⚡ Objective Tests</h4>
    </div>
    """, unsafe_allow_html=True)

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("Speed 5m", f"{pdata['speed5m']}s")
    mcol2.metric("Speed 10m", f"{pdata['speed10m']}s")
    mcol3.metric("Speed 15m", f"{pdata['speed15m']}s")
    mcol4.metric("Explosivity", f"{pdata['explosivity']}")
