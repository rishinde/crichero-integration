import cloudscraper
import st

url = "https://cricheroes.com/team-profile/4575270/revanta-risers-ravet-(rrr)/leaderboard"
scraper = cloudscraper.create_scraper()
response = scraper.get(url)

if response.status_code == 200:
    html = response.text
    st.write("✅ Page fetched successfully!")
else:
    st.error(f"❌ Failed to fetch page. HTTP {response.status_code}")
