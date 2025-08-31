import requests
import pandas as pd
from datetime import datetime, timedelta

# DraftKings API base
BASE_URL = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/885"

# Get tomorrow's date
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

def get_dk_props(date=tomorrow):
    # Call DK WNBA event group
    url = f"{BASE_URL}?format=json"
    r = requests.get(url).json()
    
    events = r['eventGroup']['events']
    markets = r['eventGroup']['offerCategories']
    
    data = []
    
    for event in events:
        event_date = event['startDate'][:10]
        if event_date != date:
            continue
        
        event_id = event['eventId']
        teams = event['name']
        
        # Go into player prop categories
        for cat in markets:
            if cat['name'] != "Player Props":
                continue
            
            for subcat in cat['offerSubcategoryDescriptors']:
                for offer in subcat['offerSubcategory']['offers']:
                    for market in offer:
                        if 'label' not in market: 
                            continue
                        for outcome in market['outcomes']:
                            data.append({
                                "Game": teams,
                                "EventID": event_id,
                                "Category": market['label'],
                                "Player": outcome['participant'],
                                "Line": outcome.get('line', None),
                                "Price": outcome['oddsAmerican'],
                                "BetType": outcome['label']
                            })
    
    return pd.DataFrame(data)

# Run for tomorrow
df = get_dk_props()
print(df.head(30))
df.to_csv("DK_WNBA_Tomorrow.csv", index=False)

