import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from cricheroes import Team

st.set_page_config(page_title="CricHeroes Team Viewer", page_icon="🏏", layout="centered")
st.title("🏏 CricHeroes Team Viewer 🏏")

# -----------------------------
# Configure Chrome for Streamlit Cloud
# -----------------------------
CHROME_BIN = "/usr/bin/chromium"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = CHROME_BIN

service = Service(CHROMEDRIVER_PATH)

# -----------------------------
# User Input
# -----------------------------
team_url = st.text_input("Enter CricHeroes Team URL (e.g., 2580003/CP-Sm@shers):", "")

if st.button("Load Team Players") and team_url:
    try:
        # Create Selenium driver manually
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Pass driver session into Team
        team = Team(url=team_url, driver=driver)

        # --- Get players ---
        players = team.get_players()
        if not players:
            st.warning("⚠️ No players found — check team URL or CricHeroes availability.")
        else:
            st.success(f"✅ Loaded {len(players)} players")
            df = pd.DataFrame([{"Player Name": p.name} for p in players])
            df.index += 1
            df.index.name = "S.No"
            st.dataframe(df)

        # --- Get matches (optional) ---
        matches = team.get_matches()
        if matches:
            st.subheader("Recent Matches")
            df_matches = pd.DataFrame([{"Date": m.date, "Result": m.result} for m in matches])
            df_matches.index += 1
            df_matches.index.name = "S.No"
            st.dataframe(df_matches)

        driver.quit()

    except Exception as e:
        st.error(f"❌ Failed to load team: {e}")
