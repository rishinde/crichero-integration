import streamlit as st
import pandas as pd
from cricheroes import Team

st.set_page_config(page_title="CricHeroes Team Viewer", page_icon="🏏", layout="centered")
st.title("🏏 CricHeroes Team Viewer 🏏")

st.markdown("### Enter your CricHeroes Team URL")
team_url = st.text_input(
    "Example: https://cricheroes.in/team-profile/2580003/CP-Sm@shers",
    ""
)

if st.button("Load Team Players") and team_url:
    try:
        # Clean up URL if user pasted full link
        team_url = team_url.strip().replace("https://cricheroes.in/team-profile/", "").strip("/")

        # Instantiate team directly (library handles Selenium)
        team = Team(url=team_url)

        # Fetch players
        players = team.get_players()

        if not players:
            st.warning("⚠️ No players found. Double-check your CricHeroes team link.")
        else:
            st.success(f"✅ Loaded {len(players)} players!")
            df = pd.DataFrame([{"Player Name": p.name} for p in players])
            df.index += 1
            df.index.name = "S.No"
            st.dataframe(df)

        # Optionally show matches
        matches = team.get_matches()
        if matches:
            st.subheader("Recent Matches")
            df_matches = pd.DataFrame([
                {"Date": m.date, "Result": m.result}
                for m in matches
            ])
            df_matches.index += 1
            df_matches.index.name = "S.No"
            st.dataframe(df_matches)

    except Exception as e:
        st.error(f"❌ Failed to load team: {e}")
