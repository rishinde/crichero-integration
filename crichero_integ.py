import streamlit as st
import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup

st.set_page_config(page_title="🏏 CricHeroes Team Viewer", page_icon="🏏", layout="centered")

st.title("🏏 CricHeroes Team Viewer (CricHeroes Integration)")
st.markdown("Enter your **CricHeroes Team URL** below to fetch the player list:")

team_url = st.text_input(
    "Example: https://cricheroes.in/team-profile/2580003/CP-Sm@shers",
    ""
)

if st.button("Load Team Players") and team_url:
    try:
        scraper = cloudscraper.create_scraper()  # Bypass Cloudflare & bot detection
        response = scraper.get(team_url)

        if response.status_code != 200:
            st.error(f"❌ Failed to fetch page. HTTP {response.status_code}")
        else:
            soup = BeautifulSoup(response.text, "html.parser")

            # Look for various player selectors that CricHeroes uses
            player_elements = soup.select("div.player-name, div.player-profile-name, h5.player-name, span.player-name")

            players = [p.get_text(strip=True) for p in player_elements if p.get_text(strip=True)]
            players = list(dict.fromkeys(players))  # remove duplicates

            if not players:
                st.warning("⚠️ No players found. The CricHeroes page structure may have changed.")
            else:
                st.success(f"✅ Loaded {len(players)} players successfully!")
                df = pd.DataFrame({"Player Name": sorted(players)})
                df.index += 1
                df.index.name = "S.No"
                st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Failed to load team: {e}")
