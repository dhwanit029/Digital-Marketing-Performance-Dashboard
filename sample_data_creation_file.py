import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for consistent results
np.random.seed(42)

# Generate 365 days of dates (1 year)
start_date = datetime.now() - timedelta(days=365)
dates = [start_date + timedelta(days=x) for x in range(365)]
date_list = np.random.choice(dates, 5000)  # 5,000 ad records

# 12 Marketing Agency Clients (exactly like real agencies)
clients = ['ClientA', 'ClientB', 'ClientC', 'ClientD', 'ClientE', 
           'ClientF', 'ClientG', 'ClientH', 'ClientI', 'ClientJ', 
           'ClientK', 'ClientL']

# Realistic campaign names
google_campaigns = ['Search-Brand', 'Search-Nonbrand', 'Display-Prospecting', 
                   'YouTube-Awareness', 'Shopping-Products']
fb_campaigns = ['FB-Prospecting', 'FB-Remarketing', 'IG-Stories', 
                'FB-Video', 'Messenger']

platforms = ['Google Ads', 'Facebook Ads']

# Generate realistic ad data
data = []
for i in range(5000):
    client = random.choice(clients)
    platform = random.choice(platforms)
    campaign_base = random.choice(google_campaigns if platform == 'Google Ads' else fb_campaigns)
    campaign_name = f"{client}-{campaign_base}"
    
    date = date_list[i].strftime('%Y-%m-%d')
    
    # Realistic metrics
    impressions = random.randint(500, 50000)
    clicks = int(impressions * random.uniform(0.01, 0.08))  # CTR 1-8%
    cost = round(clicks * random.uniform(0.50, 5.00), 2)     # CPC $0.50-$5
    conversions = random.randint(0, max(1, clicks//20))      # ~5% conversion rate
    
    data.append({
        'date': date,
        'client': client,
        'platform': platform,
        'campaign': campaign_name,
        'impressions': impressions,
        'clicks': clicks,
        'cost': cost,
        'conversions': conversions
    })

# Create DataFrame
df = pd.DataFrame(data)

# Calculate key metrics
df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
df['cpc'] = (df['cost'] / df['clicks']).round(2)
df['cpa'] = np.where(df['conversions'] > 0, (df['cost'] / df['conversions']).round(2), 0)

# Holiday boost (Nov-Dec: 60% higher spend)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
holiday_boost = df['month'].apply(lambda x: 1.6 if x in [11,12] else 1.0)
df['cost'] = (df['cost'] * holiday_boost).round(2)
df['impressions'] = (df['impressions'] * holiday_boost).round(0)

# Save to CSV
df.to_csv('marketing_agency_ads_data.csv', index=False)

# Show results
print(f"✅ SUCCESS! Generated {len(df):,} realistic ad records")
print(f"📊 12 Clients: {', '.join(clients)}")
print(f"💰 Total Spend: ${df['cost'].sum():,.0f}")
print(f"🎯 Total Conversions: {df['conversions'].sum():,}")
print(f"💵 Avg CPA: ${df['cpa'].mean():.2f}")
print("\nFirst 10 rows:")
print(df.head(10))
