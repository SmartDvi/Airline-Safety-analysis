import os
import pandas as pd
import numpy as np

colors = {
    'background': '#F8F9FA',
    'card_bg': '#FFFFFF',
    'card_border': '#E9ECEF',
    'primary': '#2C5AA0',
    'secondary': '#6C757D',
    'success': '#198754',
    'warning': '#FFC107',
    'danger': '#DC3545',
    'text_primary': '#212529',
    'text_secondary': '#6C757D',
    'accent': '#0DCAF0',
    'accent_gradient': 'linear-gradient(135deg, #2C5AA0 0%, #0DCAF0 100%)'
}

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "airline-safety.csv")

df = pd.read_csv(csv_path)

# Add calculated metrics
df_wide = df.copy()
df_wide["incident_rate_85_99"] = df_wide["incidents_85_99"] / df_wide["avail_seat_km_per_week"] * 1e9
df_wide["incident_rate_00_14"] = df_wide["incidents_00_14"] / df_wide["avail_seat_km_per_week"] * 1e9

df_wide["fatality_rate_85_99"] = df_wide["fatalities_85_99"] / df_wide["avail_seat_km_per_week"] * 1e9
df_wide["fatality_rate_00_14"] = df_wide["fatalities_00_14"] / df_wide["avail_seat_km_per_week"] * 1e9

df_wide["fatal_accident_rate_85_99"] = df_wide["fatal_accidents_85_99"] / df_wide["avail_seat_km_per_week"] * 1e9
df_wide["fatal_accident_rate_00_14"] = df_wide["fatal_accidents_00_14"] / df_wide["avail_seat_km_per_week"] * 1e9

# Custom safety score (lower is safer)
df_wide["safety_score"] = (
    df_wide["incident_rate_85_99"] * 0.3 +
    df_wide["incident_rate_00_14"] * 0.3 +
    df_wide["fatality_rate_85_99"] * 0.2 +
    df_wide["fatality_rate_00_14"] * 0.2
)

df_wide["safety_rank"] = df_wide["safety_score"].rank(method="dense")

df_wide = df_wide.rename(columns={
    'incidents_85_99': 'incidents_1985_1999',
    'fatal_accidents_85_99': 'fatal_accidents_1985_1999',
    'fatalities_85_99': 'fatalities_1985_1999',
    'incidents_00_14': 'incidents_2000_2014',
    'fatal_accidents_00_14': 'fatal_accidents_2000_2014',
    'fatalities_00_14': 'fatalities_2000_2014',
    'incident_rate_85_99': 'incident_rate_1985_1999',
    'incident_rate_00_14': 'incident_rate_2000_2014',
    'fatality_rate_85_99': 'fatality_rate_1985_1999',
    'fatality_rate_00_14': 'fatality_rate_2000_2014',
    'fatal_accident_rate_85_99': 'fatal_accident_rate_1985_1999',
    'fatal_accident_rate_00_14': 'fatal_accident_rate_2000_2014'
})

# Melting the dataset for more insights
df_long = df.melt(
    id_vars=["airline", "avail_seat_km_per_week"],
    value_vars=[
        "incidents_85_99", "fatal_accidents_85_99", "fatalities_85_99",
        "incidents_00_14", "fatal_accidents_00_14", "fatalities_00_14",
    ],
    var_name="metric",
    value_name="value"
)

df_long["period"] = df_long["metric"].apply(
    lambda x: "1985-1999" if "85_99" in x else "2000-2014"
)

df_long["metric_type"] = df_long["metric"].apply(
    lambda x: x.replace("_85_99", "").replace("_00_14", "")
)

df_long.drop(columns=["metric"], inplace=True)

# Risk categorization
airline_totals = df_long.groupby('airline')['value'].sum().fillna(0)
risk_bins = [0, 5, 20, float('inf')]
risk_labels = ['Low Risk', 'Medium Risk', 'High Risk']
risk_categories = pd.cut(airline_totals, bins=risk_bins, labels=risk_labels)
df_long['risk_category'] = df_long['airline'].map(risk_categories).fillna('Low Risk')

# Improvement status
airline_period_summary = df_long.groupby(['airline', 'period'])['value'].sum().unstack()
if '1985-1999' in airline_period_summary.columns and '2000-2014' in airline_period_summary.columns:
    airline_period_summary['improvement_status'] = np.where(
        airline_period_summary['2000-2014'] < airline_period_summary['1985-1999'],
        'Improved', 
        'Worsened'
    )
else:
    airline_period_summary['improvement_status'] = 'No Data'

df_long['improvement_status'] = df_long['airline'].map(
    airline_period_summary['improvement_status']
).fillna('No Data')

# Get unique values for filters
available_periods = sorted([p for p in df_long['period'].unique() if pd.notna(p)])
available_metrics = sorted([m for m in df_long['metric_type'].unique() if pd.notna(m)])
available_risk_categories = sorted([r for r in df_long['risk_category'].unique() if pd.notna(r)])
available_improvement_status = sorted([i for i in df_long['improvement_status'].unique() if pd.notna(i)])
available_airlines = sorted([a for a in df_long['airline'].unique() if pd.notna(a)])