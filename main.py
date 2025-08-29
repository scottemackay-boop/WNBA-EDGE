import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import json

# =========================
# 1. WNBA.com - Game Logs & Splits
# =========================
def get_wnba_game_logs(player_id, season="2025"):
    """
    Pull game logs for a given player from WNBA Stats API.
    """
    url = f"https://stats.wnba.com/stats/playergamelogs?PlayerID={player_id}&Season={season}&SeasonType=Regular+Season"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers).json()

    headers_data = resp['resultSets'][0]['headers']
    rows = resp['resultSets'][0]['rowSet']
    df = pd.DataFrame(rows, columns=headers_data)
    return df


def get_wnba_splits(player_id, season="2025"):
    """
    Pull player splits (home/away, win/loss, etc.).
    """
    url = f"https://stats.wnba.com/stats/playerdashboardbygeneralsplits?PlayerID={player_id}&Season={season}&SeasonType=Regular+Season"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers).json()

    headers_data = resp['resultSets'][1]['headers']
    rows = resp['resultSets'][1]['rowSet']
    df = pd.DataFrame(rows, columns=headers_data)
    return df


# =========================
# 2. HerHoopStats - Advanced Box Scores
# =========================
def scrape_herhoopstats_boxscore(game_url):
    """
    Scrape advanced box score data from HerHoopStats.
    Example game_url: "https://herhoopstats.com/boxscore/wnba/game_id"
    """
    resp = requests.get(game_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "lxml")

    tables = soup.find_all("table")
    dfs = pd.read_html(str(tables))
    return dfs  # list of DataFrames for each team


# =========================
# 3. Covers / FanDuel / DraftKings / Hardbooks
# =========================
def scrape_covers_player_props():
    url = "https://www.covers.com/sport/basketball/wnba/player-props"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "lxml")

    props = []
    for row in soup.select(".covers-CoversOdds-datavalue"):
        props.append(row.text.strip())
    return props


def get_fanduel_props():
    url = "https://sportsbook.fanduel.com/cache/psevent/..."  # real API endpoints rotate
    # Placeholder: in practice you’d hit their JSON endpoints (FanDuel, DK, Caesars all have hidden APIs)
    return {}


# =========================
# 4. PrizePicks Daily Lines
# =========================
def get_prizepicks_lines():
    url = "https://api.prizepicks.com/projections"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()

    data = resp["data"]
    projections = []
    for item in data:
        player = item["attributes"]["athlete_name"]
        stat = item["attributes"]["stat_type"]
        line = item["attributes"]["line_score"]
        projections.append({"player": player, "stat": stat, "line": line})
    return pd.DataFrame(projections)


# =========================
# RUN EVERYTHING
# =========================
if __name__ == "__main__":
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Example: get Ariel Atkins game logs
    # (replace with actual PlayerID from WNBA.com stats)
    try:
        logs = get_wnba_game_logs(player_id="202250")  
        logs.to_csv(f"data/gamelogs_{today}.csv", index=False)
    except:
        print("WNBA logs not pulled - check PlayerID.")

    # PrizePicks
    try:
        pp = get_prizepicks_lines()
        pp.to_csv(f"data/prizepicks_{today}.csv", index=False)
    except:
        print("PrizePicks fetch failed.")

    # Covers odds
    try:
        covers = scrape_covers_player_props()
        print("Sample Covers odds:", covers[:10])
    except:
        print("Covers scrape failed.")
