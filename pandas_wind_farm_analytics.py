import pandas as pd
import numpy as np

def generate_wind_data(n_days=30):
    """Generates synthetic hourly wind speed and power generation data."""
    dates = pd.date_range(start='2025-01-01', periods=n_days*24, freq='h')
    
    wind_speed = np.abs(np.random.normal(7.5, 2.8, n_days*24))
    
    power = np.where((wind_speed > 3) & (wind_speed < 25), 
                     (wind_speed**3) * 0.5, 0)
    
    power += np.random.normal(0, 5, n_days*24)
    power[np.random.randint(0, n_days*24, 20)] = np.nan

    return pd.DataFrame({
        "timestamp": dates,
        "wind_speed_ms": wind_speed,
        "power_kw": power
    })

df = generate_wind_data(n_days=60)

print("  Wind Farm Analytics (Pandas)  ")

df.set_index('timestamp', inplace=True)
df['power_kw'] = df['power_kw'].interpolate(method='time').clip(lower=0)

daily_farm_report = df.resample('D').agg({
    'wind_speed_ms': ['mean', 'max'],
    'power_kw': ['sum', 'mean']
})

df['efficiency_metric'] = df['power_kw'] / (df['wind_speed_ms'] + 1)
high_performance_days = daily_farm_report[daily_farm_report[('power_kw', 'sum')] > 1200]

print(f"Total Dataset Rows: {len(df)}")
print(f"Total Power Generated (60 days): {df['power_kw'].sum():,.2f} kWh")
print("\n Top 5 Peak Performance Days:")
print(high_performance_days.head(5))

print("\n Daily Report Generated and Interpolated Successfully.")
