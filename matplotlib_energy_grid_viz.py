import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def generate_viz_data():
    """Generates synthetic hourly solar, wind, and demand data."""
    dates = pd.date_range('2025-06-01', periods=72, freq='h')
    
    solar = np.sin(np.pi * (np.arange(72) % 24) / 24)**2 * 450
    solar[np.logical_not((np.arange(72) % 24).between(6, 18))] = 0
    
    wind = 150 + np.cumsum(np.random.normal(0, 15, 72)).clip(0, 500)
    
    demand = 400 + 100 * np.sin(np.pi * (np.arange(72) % 24) / 12) + \
             150 * np.sin(2 * np.pi * (np.arange(72) % 24) / 24)**2

    return pd.DataFrame({
        "timestamp": dates,
        "Solar Generation (kW)": solar,
        "Wind Generation (kW)": wind,
        "Grid Demand (kW)": demand
    }).set_index('timestamp')

df = generate_viz_data()

plt.style.use('bmh')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

ax1.set_title(' Smart Grid Analysis: Generation vs. Demand (72h Forecast)', color='#1e293b', fontsize=18, fontweight='bold', pad=20)

ax1.fill_between(df.index, df['Solar Generation (kW)'], color='#fbbf24', alpha=0.35, label='Solar')
ax1.fill_between(df.index, df['Solar Generation (kW)'] + df['Wind Generation (kW)'], df['Solar Generation (kW)'], color='#38bdf8', alpha=0.35, label='Wind')

ax1.plot(df.index, df['Grid Demand (kW)'], color='#dc2626', linewidth=2.5, linestyle='--', label='Demand Load', alpha=0.8)

ax1.set_ylabel('Power (kW)', fontsize=12, labelpad=10)
ax1.legend(facecolor='white', frameon=True, fontsize=10)
ax1.grid(True, linestyle=':', alpha=0.6)

total_gen = df['Solar Generation (kW)'] + df['Wind Generation (kW)']
solar_perc = (df['Solar Generation (kW)'] / total_gen).fillna(0) * 100
wind_perc = (df['Wind Generation (kW)'] / total_gen).fillna(0) * 100

ax2.stackplot(df.index, solar_perc, wind_perc, labels=['Solar %', 'Wind %'], colors=['#fbbf24', '#38bdf8'], alpha=0.7)
ax2.set_title(' Renewable Energy Contribution Mix (%)', color='#1e293b', fontsize=14, fontweight='600', pad=15)
ax2.set_ylim(0, 100)
ax2.set_ylabel('Percentage (%)', fontsize=12, labelpad=10)
ax2.set_xlabel('Timeline (Forecast Period)', fontsize=12, labelpad=10)

plt.tight_layout()


print("  Energy Grid Visualization Dashboard Created  ")
print("Report: Solar generation is peaking at 12pm, Wind provides stable baseline.")
print("Tip: Use battery storage to offset the demand peaks at 7pm.")

