
# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Loading datasets
vehicle_df = pd.read_csv(r"C:\Users\Dell i3\Downloads\Project EV\Datasets\bilsalg_data.csv")
energy_df = pd.read_excel(r"C:\Users\Dell i3\Downloads\Project EV\Datasets\energy_data.xlsx")
emission_df = pd.read_excel(r"C:\Users\Dell i3\Downloads\Project EV\Datasets\emission_data.xlsx")

# Displaying the first few rows of each dataset
vehicle_df.head()
energy_df.head()

emission_df.fillna(0, inplace=True)
emission_df.head()

# Structure the EV dataset
# EV
vehicle_df['EV_New'] = vehicle_df['BEV: New']
vehicle_df['EV_Used'] = vehicle_df['BEV: Used']

# ICE (Petrol + Diesel + Hybrids)
vehicle_df['ICE_New'] = (vehicle_df['PetrolOnly: New'] + 
                         vehicle_df['DieselOnly: New'] + 
                         vehicle_df['Non-plugin hybrid: New'] + 
                         vehicle_df['Plugin hybrid: New'])

vehicle_df['ICE_Used'] = (vehicle_df['PetrolOnly: Used'] + 
                          vehicle_df['DieselOnly: Used'] + 
                          vehicle_df['Non-plugin hybrid: Used'] + 
                          vehicle_df['Plugin hybrid: Used'])

vehicle_df['EV_Total'] = vehicle_df['EV_New'] + vehicle_df['EV_Used']
vehicle_df['ICE_Total'] = vehicle_df['ICE_New'] + vehicle_df['ICE_Used']

vehicle_df['Year'] = vehicle_df['YYYYMM'].astype(str).str[:4]
yearly_summary = vehicle_df.groupby('Year')[['EV_Total', 'ICE_Total']].sum().reset_index()
# Calculate EV Share (%)
yearly_summary['EV_Share'] = (
    yearly_summary['EV_Total'] / 
    (yearly_summary['EV_Total'] + yearly_summary['ICE_Total'])
) * 100
yearly_summary.head()
# How fast EV share is growing
import matplotlib.pyplot as plt
yearly_summary['Year'] = pd.to_numeric(yearly_summary['Year'])
plt.figure(figsize=(8,5))
plt.plot(yearly_summary['Year'], yearly_summary['EV_Share'], marker='o')

plt.title("EV Share of Total Vehicles Over Time (Norway)")
plt.xlabel("Year")
plt.ylabel("EV Share (%)")
plt.xlim(1990,2026)
plt.grid(True)
plt.show()

# How ICE vs EV volumes are trending
plt.figure(figsize=(10,6))
plt.plot(yearly_summary['Year'], yearly_summary['EV_Total'], label="EV", marker='o')
plt.plot(yearly_summary['Year'], yearly_summary['ICE_Total'], label="ICE", marker='o')

plt.title("EV vs ICE Registrations in Norway")
plt.xlabel("Year")
plt.ylabel("Number of Vehicles")
plt.legend()
plt.xlim(1990,2026)
plt.grid(True)
plt.show()

# Modeling from prophet


# Example: your base data (replace with your real data)
web_data = {
    "avg_km_per_car": 12000,     # yearly km driven per car
    "kWh_per_km_EV": 0.18,       # avg EV consumption
    "l_per_km_ICE": 0.07,        # avg ICE fuel consumption
    "CO2_per_litre": 2.31        # kg CO2 per litre petrol/diesel
}


def calculate_impacts(yearly_summary):
    # Annual estimated values
    web_data = {
        "avg_km_per_car": 12000,
        "kWh_per_km_EV": 0.18,
        "l_per_km_ICE": 0.07,
        "CO2_per_litre": 2.31
    }

    # Measures
    # Calculate EV Share (%) of total vehicles
    yearly_summary["EV_Share"] = (
        yearly_summary["EV_Total"] /
    (yearly_summary["EV_Total"] + yearly_summary["ICE_Total"])
    ) * 100

    yearly_summary["EV_Energy_Demand_kWh"] = (
        yearly_summary["EV_Total"] * web_data["avg_km_per_car"] * web_data["kWh_per_km_EV"]
    )
    yearly_summary["ICE_Fuel_Demand_L"] = (
        yearly_summary["ICE_Total"] * web_data["avg_km_per_car"] * web_data["l_per_km_ICE"]
    )
    yearly_summary["ICE_CO2_Emissions_kg"] = (
        yearly_summary["ICE_Fuel_Demand_L"] * web_data["CO2_per_litre"]
    )
    yearly_summary["ICE_CO2_Emissions_tonnes"] = yearly_summary["ICE_CO2_Emissions_kg"] / 1000
    yearly_summary["Net_CO2_Savings_kg"] = yearly_summary["ICE_CO2_Emissions_kg"]

    # Aggregate totals
    totals = {
        "ev_total": int(yearly_summary["EV_Total"].sum()),
        "ice_total": int(yearly_summary["ICE_Total"].sum()),
        "ev_energy": int(yearly_summary["EV_Energy_Demand_kWh"].sum()),
        "ice_fuel": int(yearly_summary["ICE_Fuel_Demand_L"].sum()),
        "ice_co2_kg": int(yearly_summary["ICE_CO2_Emissions_kg"].sum()),
        "ice_co2_tonnes": int(yearly_summary["ICE_CO2_Emissions_tonnes"].sum()),
        "net_co2_savings": int(yearly_summary["Net_CO2_Savings_kg"].sum())
    }

    return yearly_summary, totals


print(yearly_summary.head())

yearly_summary, totals = calculate_impacts(yearly_summary)


# Line chart: Energy demand
plt.figure(figsize=(10,6))
plt.plot(yearly_summary["Year"], yearly_summary["EV_Energy_Demand_kWh"], label="EV Energy Demand (kWh)", marker="o")
plt.plot(yearly_summary["Year"], yearly_summary["ICE_Fuel_Demand_L"], label="ICE Fuel Demand (Litres)", marker="s")
plt.xlabel("Year")
plt.ylabel("Demand")
plt.title("Energy Demand: EV vs ICE")
plt.xlim(1990,2026)
plt.legend()
plt.show()

# Bar chart: CO2 emissions
plt.figure(figsize=(10,6))
plt.bar(yearly_summary["Year"], yearly_summary["ICE_CO2_Emissions_tonnes"], color="red", alpha=0.7, label="ICE CO2 Emissions")
plt.xlabel("Year")
plt.ylabel("CO₂ Emissions (tonnes)")
plt.title("ICE Vehicle CO₂ Emissions Over Time")
plt.legend()
plt.xlim(1990,2026)
plt.show()

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

X = yearly_summary["Year"].values.reshape(-1, 1)
y = yearly_summary["EV_Total"] / (yearly_summary["EV_Total"] + yearly_summary["ICE_Total"])

# Train/test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print(energy_df["Variable"].unique())   # See all unique energy types

# ---- Extract only energy generation related rows ----
# Example: Keep only rows where Category = 'Electricity generation'
gen_df = energy_df[energy_df["Category"].str.contains("generation", case=False, na=False)]

# ---- Get unique energy sources ----
energy_sources = gen_df["Subcategory"].unique()
print("Energy generation types:", energy_sources)

# ---- Group by Subcategory and sum values ----
energy_summary = gen_df.groupby("Subcategory")["Value"].sum().reset_index()
print(energy_summary)

# ---- Optional: Pivot table for Yearly energy generation by Subcategory ----
energy_by_year = gen_df.pivot_table(
    index="Year", 
    columns="Variable", 
    values="Value", 
    aggfunc="sum"
).reset_index()

print(energy_by_year.head())

# Define mapping
renewables = [
    "Renewables", "Wind", "Solar", "Hydro", "Bioenergy", 
    "Other Renewables", "Wind and Solar", "Hydro, Bioenergy and Other Renewables"
]

non_renewables = [
    "Coal", "Gas", "Fossil", "Other Fossil", "Gas and Other Fossil"
]

# Function to classify
def classify_energy(var):
    if var in renewables:
        return "Renewable"
    elif var in non_renewables:
        return "Non-Renewable"
    else:
        return "Other"

# Apply classification
energy_df["Energy_Category"] = energy_df["Variable"].apply(classify_energy)

# Check counts
print(energy_df["Energy_Category"].value_counts())

# Group total values
summary = energy_df.groupby("Energy_Category")["Value"].sum().reset_index()
print(summary)

import matplotlib.pyplot as plt

# Bar chart
plt.figure(figsize=(6,4))
plt.bar(summary["Energy_Category"], summary["Value"], color=["green", "red", "gray"])
plt.title("Total Energy by Category")
plt.xlabel("Energy Category")
plt.ylabel("Total Value")
plt.show()

# Pie chart
plt.figure(figsize=(6,6))
plt.pie(summary["Value"], labels=summary["Energy_Category"], autopct="%1.1f%%", 
        colors=["green", "red", "gray"], startangle=90, wedgeprops={"edgecolor":"black"})
plt.title("Energy Distribution: Renewable vs Non-Renewable")
plt.show()

# Filter renewable data
renewable_summary = (
    energy_df[energy_df["Energy_Category"] == "Renewable"]
    .groupby("Variable")["Value"].sum()
    .reset_index()
)

# Filter non-renewable data
nonrenewable_summary = (
    energy_df[energy_df["Energy_Category"] == "Non-Renewable"]
    .groupby("Variable")["Value"].sum()
    .reset_index()
)

# Plot renewables
plt.figure(figsize=(8,4))
plt.bar(renewable_summary["Variable"], renewable_summary["Value"], color="green")
plt.title("Breakdown of Renewable Energy Sources")
plt.xlabel("Source")
plt.ylabel("Total Value")
plt.xticks(rotation=30)
plt.show()

# Plot non-renewables
plt.figure(figsize=(6,4))
plt.bar(nonrenewable_summary["Variable"], nonrenewable_summary["Value"], color="red")
plt.title("Breakdown of Non-Renewable Energy Sources")
plt.xlabel("Source")
plt.ylabel("Total Value")
plt.xticks(rotation=30)
plt.show()

# Make year is integer
emission_df["year"] = emission_df["year"].astype(int)

# CO2 emissions
plt.figure(figsize=(10,6))
plt.plot(emission_df["year"], emission_df["co2"], marker="", linestyle="-", color="red")
plt.title("CO₂ Emissions Over Years", fontsize=14)
plt.xlabel("Year")
plt.ylabel("CO₂ Emissions (MtCO₂)")
plt.xlim(1900, 2025)
plt.grid(True)
plt.show()

km_per_year = 15000
emission_rate_ice = 0.21  # kg CO2/km
emission_rate_ev = 0.08   # kg CO2/km

ice_emissions = emission_rate_ice * km_per_year  # ~3150 kg/year
ev_emissions = emission_rate_ev * km_per_year    # ~1200 kg/year
savings_per_car = ice_emissions - ev_emissions   # ~1950 kg/year

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

# --- Custom Transformer for Emissions ---
class EmissionsCalculator(BaseEstimator, TransformerMixin):
    def __init__(self, km_per_year=15000, emission_rate_ice=0.21, emission_rate_ev=0.08):
        self.km_per_year = km_per_year
        self.emission_rate_ice = emission_rate_ice
        self.emission_rate_ev = emission_rate_ev

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        # Make sure required columns exist
        if not {"EV_Total", "ICE_Total"}.issubset(df.columns):
            raise ValueError("DataFrame must have columns: 'EV_Total' and 'ICE_Total'")
        
        df["ICE_CO2_Emissions_kg"] = (
            df["ICE_Total"] * self.km_per_year * self.emission_rate_ice
        )
        df["EV_CO2_Emissions_kg"] = (
            df["EV_Total"] * self.km_per_year * self.emission_rate_ev
        )
        df["Net_CO2_Savings_kg"] = (
            df["ICE_CO2_Emissions_kg"] - df["EV_CO2_Emissions_kg"]
        )
        return df

# --- Example Usage ---
if __name__ == "__main__":
    # 🚗 Replace this with your actual DataFrame
    vehicle_data = pd.DataFrame({
        "Year": [2025, 2026, 2027],
        "EV_Total": [5000, 8000, 12000],
        "ICE_Total": [20000, 21000, 22000],
    })

    # Define pipeline
    pipeline = Pipeline([
        ("emissions", EmissionsCalculator(
            km_per_year=15000, 
            emission_rate_ice=0.21, 
            emission_rate_ev=0.08
        ))
    ])

    # Transform your dataset
    results = pipeline.fit_transform(vehicle_data)

    print(results)

def run_analysis():
    return f"Analysis completed."