import requests
import pandas as pd

# FanDuel API endpoint for WNBA
# 1227 = WNBA league code
FANDUEL_API = "https://sportsbook.fanduel.com//cache/psmg/UK/SPORT/1227.json"

def fetch_fanduel_lines() -> pd.DataFrame:
    """
    Fetch all WNBA player props from FanDuel.
    Returns DataFrame with player, market, line, and odds.
    """
    try:
        resp = requests.get(FANDUEL_API, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"❌ Error fetching FanDuel lines: {e}")
        return pd.DataFrame()

    rows = []
    for event in data.get("events", []):
        event_name = event.get("eventName")
        for market in event.get("markets", []):
            market_name = market.get("marketName")
            for outcome in market.get("outcomes", []):
                rows.append({
                    "event": event_name,
                    "player": outcome.get("participant"),
                    "market": market_name,
                    "line": outcome.get("line"),
                    "oddsAmerican": outcome.get("oddsAmerican"),
                    "oddsDecimal": outcome.get("oddsDecimal"),
                })

    df = pd.DataFrame(rows)
    return df
