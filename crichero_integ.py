# cricheroes_team_cloud.py
import streamlit as st
from cricheroes import Team
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

st.set_page_config(page_title="CricHeroes Team", page_icon="🏏", layout="centered")
st.title("🏏 CricHeroes Team Viewer 🏏")

# -----------------------------
# Setup Chrome driver automatically
# -----------------------------
chromedriver_autoinstaller.install()  # Installs driver if not already

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# -----------------------------
# User Input
# -----------------------------
team_url = st.text_input("Enter CricHeroes Team URL (e.g., 2580003/CP-Sm@shers):", "")

if st.button("Load Team Players") and team_url:
    try:
        # Initialize Team object
        team = Team(url=team_url, driver_path=None, chrome_options=chrome_options)

        # Get players
        players = team.get_players()
        st.success(f"✅ Loaded {len(players)} players")

        df = pd.DataFrame([{"Player Name": p.name} for p in players])
        df.index += 1
        df.index.name = "S.No"
        st.dataframe(df)

        # Optional: Recent matches
        matches = team.get_matches()
        if matches:
            st.subheader("Recent Matches")
            df_matches = pd.DataFrame([{"Date": m.date, "Result": m.result} for m in matches])
            df_matches.index += 1
            df_matches.index.name = "S.No"
            st.dataframe(df_matches)

    except Exception as e:
        st.error(f"❌ Failed to load team: {e}")
