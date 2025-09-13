import streamlit as st
import os

st.title("📂 Reports & Uploads")

player = st.session_state.get("selected_player", None)
if not player:
    st.warning("Go back and select a player first.")
    st.stop()

upload = st.file_uploader("Upload PDF report", type=["pdf"])
if upload:
    path = f"data/{player}_report.pdf"
    with open(path, "wb") as f:
        f.write(upload.getbuffer())
    st.success(f"Report saved as {path}")

# List previously uploaded reports
st.subheader("Available Reports")
for file in os.listdir("data/"):
    if file.endswith("_report.pdf"):
        st.write(file)
