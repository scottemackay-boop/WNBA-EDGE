import os
import pandas as pd

# Import all scraper functions
from scrapers.wnba_gamelogs import fetch_gamelogs
from scrapers.advanced_box import fetch_advanced_box
from scrapers.prizepicks import fetch_prizepicks
from scrapers.odds import fetch_odds
from scrapers.injuries import fetch_injuries
from scrapers.pace import fetch_pace
from scrapers.usage_rates import fetch_usage_rates
from scrapers.synergy_playtypes import fetch_synergy_playtypes
from scrapers.on_off import fetch_on_off
from scrapers.rest_days import fetch_rest_days
from scrapers.weather_travel import fetch_weather_travel


def save_csv(df: pd.DataFrame, name: str):
    """Save DataFrame to /data folder."""
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", f"{name}.csv")
    df.to_csv(path, index=False)
    print(f"✅ Saved {path}")


if __name__ == "__main__":
    scrapers = {
        "gamelogs": fetch_gamelogs,
        "advanced_box": fetch_advanced_box,
        "prizepicks": fetch_prizepicks,
        "odds": fetch_odds,
        "injuries": fetch_injuries,
        "pace": fetch_pace,
        "usage_rates": fetch_usage_rates,
        "synergy_playtypes": fetch_synergy_playtypes,
        "on_off": fetch_on_off,
        "rest_days": fetch_rest_days,
        "weather_travel": fetch_weather_travel,
    }

    for name, func in scrapers.items():
        df = func()
        save_csv(df, name)
