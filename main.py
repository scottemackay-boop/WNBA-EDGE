# main.py
"""
WNBA-EDGE Main Orchestrator
Pulls gamelogs, splits, advanced box scores, PrizePicks props, sportsbook odds,
injuries, pace, usage, playtypes, and rest/travel info. Cleans and saves into /data.
"""

import os
import pandas as pd

# Import all scrapers (you’ll create these files in scrapers/)
from scrapers import (
    wnba_gamelogs,
    advanced_box,
    prizepicks,
    odds,
    injuries,
    pace,
    usage_rates,
    synergy_playtypes,
    on_off,
    rest_days,
    weather_travel
)

DATA_DIR = "data"

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def run_all_scrapers():
    ensure_data_dir()

    print("▶ Pulling WNBA Gamelogs + Splits...")
    gamelogs = wnba_gamelogs.fetch_gamelogs()
    gamelogs.to_csv(f"{DATA_DIR}/gamelogs.csv", index=False)

    print("▶ Pulling Advanced Box Scores...")
    adv_box = advanced_box.fetch_advanced()
    adv_box.to_csv(f"{DATA_DIR}/advanced_box.csv", index=False)

    print("▶ Pulling PrizePicks Board...")
    pp = prizepicks.fetch_prizepicks()
    pp.to_csv(f"{DATA_DIR}/prizepicks.csv", index=False)

    print("▶ Pulling Sportsbook Odds (FD/DK/Covers)...")
    books = odds.fetch_odds()
    books.to_csv(f"{DATA_DIR}/odds_books.csv", index=False)

    print("▶ Pulling Injuries...")
    inj = injuries.fetch_injuries()
    inj.to_csv(f"{DATA_DIR}/injuries.csv", index=False)

    print("▶ Pulling Pace Stats...")
    pace_stats = pace.fetch_pace()
    pace_stats.to_csv(f"{DATA_DIR}/pace.csv", index=False)

    print("▶ Pulling Usage Rates...")
    usage = usage_rates.fetch_usage()
    usage.to_csv(f"{DATA_DIR}/usage.csv", index=False)

    print("▶ Pulling Playtype Data...")
    playtypes = synergy_playtypes.fetch_playtypes()
    playtypes.to_csv(f"{DATA_DIR}/playtypes.csv", index=False)

    print("▶ Pulling On/Off Splits...")
    onoff = on_off.fetch_onoff()
    onoff.to_csv(f"{DATA_DIR}/onoff.csv", index=False)

    print("▶ Pulling Rest/Days + Travel Info...")
    rest = rest_days.fetch_rest()
    travel = weather_travel.fetch_travel()
    rest.to_csv(f"{DATA_DIR}/rest_days.csv", index=False)
    travel.to_csv(f"{DATA_DIR}/travel.csv", index=False)

    print("✅ All data pulled + saved to /data")

if __name__ == "__main__":
    run_all_scrapers()
