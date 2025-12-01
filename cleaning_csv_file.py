import pandas as pd
import numpy as np
import os
from pathlib import Path

# File paths - UPDATE THESE TO YOUR ACTUAL FILE PATHS
input_file = r"D:\Marketing Agency sample project Dashboard\marketing_agency_ads_data.csv"  # Your input file path
output_file = r"D:\Marketing Agency sample project Dashboard\cleaned_marketing_agency_ads_data.csv"  # Output cleaned file path

# Load data
df = pd.read_csv(input_file)
print(f"Loaded {len(df)} rows from {input_file}")

# 1. Extract client name from campaign (before first '-')
df['extracted_client'] = df['campaign'].str.split('-').str[0]

# 2. Categorize campaign based on naming pattern
def categorize_campaign(campaign_name):
    if pd.isna(campaign_name):
        return 'Unknown'
    parts = str(campaign_name).split('-')
    if len(parts) >= 2:
        ad_type = parts[1].lower()
        if 'search' in ad_type:
            return 'Search'
        elif 'display' in ad_type:
            return 'Display'
        elif 'video' in ad_type:
            return 'Video'
        else:
            return 'Other'
    return 'Brand' if any('brand' in part.lower() for part in parts) else 'NonBrand'

df['campaign_category'] = df['campaign'].apply(categorize_campaign)

# 3. Standardize date format to YYYY-MM-DD
def standardize_date(date_str):
    if pd.isna(date_str):
        return pd.NaT
    date_str = str(date_str).strip()
    # Try multiple date formats
    for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y-%d-%m', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y']:
        try:
            return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    # Try pandas auto-parsing as fallback
    try:
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except:
        return pd.NaT

df['date_clean'] = df['date'].apply(standardize_date)

# 4. Handle missing values
# Numeric metrics: fill with 0
numeric_cols = ['impressions', 'clicks', 'cost', 'conversions']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Performance metrics: fill with column mean
perf_cols = ['ctr', 'cpc', 'cpa']
for col in perf_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    mean_val = df[col].mean()
    df[col] = df[col].fillna(mean_val)

# Client: use extracted_client if missing
df['client'] = df['client'].fillna(df['extracted_client'])

# Platform: fill common defaults if missing
df['platform'] = df['platform'].fillna('Unknown')

print("Data cleaning summary:")
print(f"- Rows with invalid dates: {(df['date_clean'].isna()).sum()}")
print(f"- Campaigns categorized: {df['campaign_category'].nunique()} categories")
print(f"- Clients extracted: {df['extracted_client'].nunique()} unique clients")

# Save cleaned data
df.to_csv(output_file, index=False)
print(f"✅ Cleaned data saved to: {os.path.abspath(output_file)}")

# Display first few rows of cleaned data
print("\nSample cleaned data:")
print(df[['date_clean', 'client', 'platform', 'campaign', 'campaign_category', 
         'impressions', 'clicks', 'cost', 'conversions', 'ctr', 'cpc', 'cpa']].head())
