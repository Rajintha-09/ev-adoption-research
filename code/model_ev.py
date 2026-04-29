from prophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import analysis_codes as ac

# -------------------------------
# Prepare EV data (2015+)
# -------------------------------
df_ev = ac.yearly_summary[['Year','EV_Total','ICE_Total']].copy()
df_ev = df_ev[(df_ev['Year'] >= 2018) & (df_ev['Year'] <= 2024)]
df_ev = df_ev.rename(columns={'Year':'ds','EV_Total':'y'})
df_ev['ds'] = pd.to_datetime(df_ev['ds'], format='%Y')
# -------------------------------
# Logistic Growth Model for EVs
# -------------------------------
cap_value = df_ev['y'].max() * 5  # capacity ~ 5x current max
df_ev['cap'] = cap_value

model = Prophet(
    growth="logistic",
    yearly_seasonality=False,
    changepoint_prior_scale=0.5
)
model.fit(df_ev)

# Forecast to 2030
future = model.make_future_dataframe(periods=10, freq='Y')
future['cap'] = cap_value
forecast = model.predict(future)

# -------------------------------
# Impact Calculations
# -------------------------------
forecast['Year'] = forecast['ds'].dt.year
forecast_ev = forecast[['Year','yhat']].copy()

# Merge with ICE data
impact_df = ac.yearly_summary.merge(forecast_ev, on="Year", how="outer")
impact_df['EV_Forecast'] = impact_df['yhat'].fillna(impact_df['EV_Total'])
impact_df['ICE_Forecast'] = impact_df['ICE_Total']

# Assumptions
co2_per_ice = 4.6        # tons CO2/year per ICE
fuel_cost_ice = 1500     # USD/year per ICE
elec_cost_ev = 600       # USD/year per EV

# EV Share of total
impact_df['Total'] = impact_df['EV_Forecast'] + impact_df['ICE_Forecast']
impact_df['EV_Share_%'] = (impact_df['EV_Forecast'] / impact_df['Total']) * 100

# CO2 reduction vs baseline ICE world
baseline_co2 = impact_df['Total'] * co2_per_ice
actual_co2 = (impact_df['ICE_Forecast'] * co2_per_ice) + (impact_df['EV_Forecast'] * 0.5)  # assume EV ~0.5 t/yr
impact_df['CO2_Avoided'] = baseline_co2 - actual_co2

# Cost savings vs baseline ICE world
baseline_cost = impact_df['Total'] * fuel_cost_ice
actual_cost = (impact_df['ICE_Forecast'] * fuel_cost_ice) + (impact_df['EV_Forecast'] * elec_cost_ev)
impact_df['Money_Saved'] = baseline_cost - actual_cost

# -------------------------------
# Evaluation
# -------------------------------
forecast_in_sample = model.predict(df_ev[['ds','cap']])
y_true = df_ev['y'].values
y_pred = forecast_in_sample['yhat'].values

mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mape = np.mean(np.abs((y_true - y_pred)/y_true))*100

print(f"In-sample MAE: {mae:.2f}")
print(f"In-sample RMSE: {rmse:.2f}")
print(f"In-sample MAPE: {mape:.2f}%")

# -------------------------------
# Visualization
# -------------------------------
plt.figure(figsize=(12,7))

# EV vs ICE forecast
plt.plot(impact_df['Year'], impact_df['EV_Forecast'], label="EV Forecast", marker='o')
plt.plot(impact_df['Year'], impact_df['ICE_Forecast'], label="ICE", marker='o')

# Highlight 2030 point
ev_2030 = impact_df.loc[impact_df['Year']==2030,'EV_Forecast'].values[0]
plt.scatter(2030, ev_2030, color='red', s=100, zorder=5)
plt.text(2030, ev_2030*1.05, f"{int(ev_2030):,} EVs", color='red', fontsize=12, ha='center')

plt.xlabel("Year")
plt.ylabel("Number of Vehicles")
plt.title("EV vs ICE Forecast with Impacts")
plt.legend()
plt.grid(True)
plt.show()

# -------------------------------
# Impact Dashboard (Improved)
# -------------------------------

fig, axes = plt.subplots(2,1, figsize=(12,10), sharex=True)

# --- (1) CO₂: Baseline vs Actual ---
axes[0].plot(impact_df['Year'], baseline_co2, label="Baseline CO₂ (ICE only)", linestyle="--", color="gray")
axes[0].plot(impact_df['Year'], actual_co2, label="Actual CO₂ (with EVs)", color="green")
axes[0].fill_between(impact_df['Year'], actual_co2, baseline_co2, color="green", alpha=0.3, label="CO₂ Avoided")
axes[0].set_ylabel("CO₂ Emissions (tons)")
axes[0].legend()
axes[0].grid(True)

# Highlight 2030 for CO₂
co2_2030 = impact_df.loc[impact_df['Year']==2030, 'CO2_Avoided'].values[0]
axes[0].scatter(2030, baseline_co2.loc[impact_df['Year']==2030], color="black", zorder=5)
axes[0].scatter(2030, actual_co2.loc[impact_df['Year']==2030], color="red", zorder=5)
axes[0].text(2030, co2_2030*1.05, f"{co2_2030/1e6:.1f}M tons avoided", ha="center", color="red")

# --- (2) Dual-axis: CO₂ Avoided vs Money Saved ---
ax1 = axes[1]
ax2 = ax1.twinx()

ax1.plot(impact_df['Year'], impact_df['CO2_Avoided']/1e6, color="green", marker="o", label="CO₂ Avoided (Million tons)")
ax2.plot(impact_df['Year'], impact_df['Money_Saved']/1e6, color="blue", marker="s", label="Money Saved (Million USD)")

ax1.set_ylabel("CO₂ Avoided (Million tons)", color="green")
ax2.set_ylabel("Money Saved (Million USD)", color="blue")
ax1.set_xlabel("Year")

# Highlight 2030 for Money Saved
money_2030 = impact_df.loc[impact_df['Year']==2030, 'Money_Saved'].values[0]
ax1.scatter(2030, co2_2030/1e6, color="red", zorder=5)
ax1.text(2030, (co2_2030/1e6)*1.05, f"{co2_2030/1e6:.1f}M tons", ha="center", color="red")

ax2.scatter(2030, money_2030/1e6, color="red", zorder=5)
ax2.text(2030, (money_2030/1e6)*1.05, f"${money_2030/1e6:.1f}M", ha="center", color="red")

# --- (3) Extra Metrics (Percentages) ---
impact_df["CO2_Reduction_%"] = (impact_df["CO2_Avoided"] / baseline_co2) * 100
impact_df["Cost_Saving_%"] = (impact_df["Money_Saved"] / baseline_cost) * 100

plt.suptitle("EV Adoption Impacts: Environmental & Economic", fontsize=14)
plt.tight_layout()
plt.show()

from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Train forecast model (2018–2024)
# -----------------------------
df_ev = ac.yearly_summary[["Year", "EV_Total", "ICE_Total"]].copy()
df_ev = df_ev[df_ev["Year"] >= 2018]

df_ev = df_ev.rename(columns={"Year": "ds", "EV_Total": "y"})
df_ev["ds"] = pd.to_datetime(df_ev["ds"], format="%Y")

cap_value = df_ev["y"].max() * 5
df_ev["cap"] = cap_value

model = Prophet(growth="logistic")
model.fit(df_ev)

# Forecast until 2030
future = model.make_future_dataframe(periods=6, freq="Y")
future["cap"] = cap_value
forecast = model.predict(future)

# -----------------------------
# Connect forecast to emissions
# -----------------------------
def estimate_emissions(forecast, ice_base, km_per_year=15000, ice_rate=0.21, ev_rate=0.08, fuel_price=1.8):
    """
    Estimate avoided CO2 and fuel costs from forecasted EV adoption.
    """
    results = []
    for idx, row in forecast.iterrows():
        year = row["ds"].year
        ev_total = int(row["yhat"])
        ice_total = max(ice_base - ev_total, 0)   # assume ICE decline as EVs rise

        ice_emissions = ice_total * km_per_year * ice_rate
        ev_emissions = ev_total * km_per_year * ev_rate
        net_savings = ice_emissions - ev_emissions

        # Avoided fuel use (L) & money saved
        avoided_fuel_l = ice_total * km_per_year * 0.07  # ICE avg L/km
        money_saved = avoided_fuel_l * fuel_price

        results.append({
            "Year": year,
            "Forecast_EV": ev_total,
            "Forecast_ICE": ice_total,
            "ICE_CO2_kg": round(ice_emissions, 2),
            "EV_CO2_kg": round(ev_emissions, 2),
            "Net_CO2_Savings_tonnes": round(net_savings / 1000, 2),
            "Economic_Savings_BillionUSD": round(money_saved / 1e9, 3)
        })

    return pd.DataFrame(results)

# Assume ICE base = last known ICE total (2024)
ice_base = int(ac.yearly_summary[ac.yearly_summary["Year"] == 2024]["ICE_Total"].values[0])

impact_df = estimate_emissions(forecast, ice_base)

print("\n=== Forecasted Impact (2018–2030) ===\n")
print(impact_df)

# -----------------------------
# Visualization
# -----------------------------
plt.figure(figsize=(9,5))
plt.plot(impact_df["Year"], impact_df["Net_CO2_Savings_tonnes"], marker="o", label="CO₂ Savings (tonnes)")
plt.xlabel("Year")
plt.ylabel("CO₂ Savings (tonnes)")
plt.title("Forecasted Carbon Emission Reduction from EV Adoption")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(9,5))
plt.plot(impact_df["Year"], impact_df["Economic_Savings_BillionUSD"], marker="s", color="green", label="Economic Savings (Billion USD)")
plt.xlabel("Year")
plt.ylabel("Economic Savings (Billion USD)")
plt.title("Economic Impact of EV Adoption")
plt.legend()
plt.grid(True)
plt.show()
