import pandas as pd

def calculate_metrics(input_csv, output_csv):
    # Load data
    df = pd.read_csv(input_csv)

    # Ensure date_clean is datetime
    df['date_clean'] = pd.to_datetime(df['date_clean'], errors='coerce')
    df = df.dropna(subset=['date_clean'])

    # Create a proper month column (first day of month)
    df['month'] = df['date_clean'].values.astype('datetime64[M]')

    # 1. Total Ad Spend
    total_ad_spend = df['cost'].sum()

    # 2. Total Leads
    total_leads = df['conversions'].sum()

    # 3. Cost Per Lead
    cost_per_lead = total_ad_spend / total_leads if total_leads != 0 else 0

    # 4. ROAS (uses CPA to estimate revenue if no explicit revenue column)
    if 'revenue' in df.columns:
        total_revenue = df['revenue'].sum()
    else:
        avg_cpa = df['cpa'].mean()
        total_revenue = total_leads * avg_cpa
    roas = (total_revenue / total_ad_spend) * 100 if total_ad_spend != 0 else 0

    # 5. Monthly aggregation
    monthly = (
        df.groupby('month')
          .agg(
              total_ad_spend=('cost', 'sum'),
              total_leads=('conversions', 'sum')
          )
          .sort_index()
    )

    monthly['cost_per_lead'] = (
        monthly['total_ad_spend'] / monthly['total_leads']
    ).replace([float('inf'), -float('inf')], 0)

    if 'revenue' in df.columns:
        monthly['total_revenue'] = (
            df.groupby('month')['revenue'].sum().reindex(monthly.index)
        )
    else:
        monthly['total_revenue'] = monthly['total_leads'] * avg_cpa

    monthly['roas'] = (
        monthly['total_revenue'] / monthly['total_ad_spend']
    ) * 100

    # Month‑over‑month % growth
    def mom(series):
        return series.pct_change().fillna(0) * 100

    monthly['mom_ad_spend_growth'] = mom(monthly['total_ad_spend'])
    monthly['mom_leads_growth'] = mom(monthly['total_leads'])
    monthly['mom_cpl_growth'] = mom(monthly['cost_per_lead'])
    monthly['mom_roas_growth'] = mom(monthly['roas'])

    # Save to CSV
    monthly.to_csv(output_csv, index=True)

    return {
        "Total_Ad_Spend": total_ad_spend,
        "Total_Leads": total_leads,
        "Cost_Per_Lead": cost_per_lead,
        "ROAS": roas,
        "MoM_Summary_File": output_csv
    }

# EDIT THESE PATHS FOR YOUR MACHINE
input_file_path = r"D:\Marketing Agency sample project Dashboard\cleaned_marketing_agency_ads_data.csv"
output_file_path = r"D:\Marketing Agency sample project Dashboard\monthly_metrics_summary.csv"

metrics = calculate_metrics(input_file_path, output_file_path)
print(metrics)








