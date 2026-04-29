# Global Model for Analyzing the Environmental and Economic Impacts of Electric Vehicle Adoption

**A research-based global modeling study on the environmental and economic impacts of electric vehicle (EV) adoption**

---

## Project Overview

This repository contains the **research paper, datasets, and Python-based models** developed for a global study analyzing the **environmental and economic impacts of Electric Vehicle (EV) adoption**.

The study models EV adoption trends, compares CO₂ emissions between Electric Vehicles (EVs) and Internal Combustion Engine (ICE) vehicles, and evaluates long-term economic implications such as energy consumption and operational costs.

**Key highlights:**
- Global EV adoption modeling using multiple datasets  
- Comparative environmental impact analysis (EV vs ICE)  
- Economic impact assessment based on energy and cost factors  
- Scenario-based forecasting and evaluation  

---

## Folder Structure
```
Ev-Global-Model/
│
├── paper/
│ └── Global_Model_EV_Adoption.pdf
│
├── dataset/
│ ├── bilsalg_data.csv # vehicle adoption data
│ ├── energy_data.xlsx # electricity generation mix
│ └── emission_data.xlsx # emission and economic factors
│
├── code/
│ ├── analysis_codes.py
│ ├── model_ev.py
│ └── app_p1.py
│
└── README.md
```
---

## Datasets

This study uses **three datasets** to support global modeling and analysis:

1. **`bilsalg_data.csv`**  
   Historical and projected Electric Vehicle (EV) and ICE vehicle adoption data used for trend analysis and forecasting.

2. **`energy_data.xlsx`**  
   Electricity generation mix data for estimating indirect emissions from EV charging.

3. **`emission_data.xlsx`**  
   Contains CO₂, NOx, SOx emission factors, fuel consumption rates, electricity costs, and other economic parameters required for environmental and cost impact analysis.

All datasets are cleaned, validated, and standardized prior to model implementation.

---

## Code Description

- **analysis_codes.py**  
  Performs data preprocessing, exploratory data analysis, and validation of EV adoption, emissions, and economic indicators.

- **model_ev.py**  
  Implements the core global EV adoption model, including emission calculations and economic impact estimation.

- **app_p1.py**  
  Runs integrated scenario-based simulations as described in the research paper.

---

## Methodology

- Analysis of historical EV and ICE vehicle adoption data  
- Forecasting EV adoption using mathematical and statistical models  
- Environmental impact assessment using CO₂ emission factors and electricity mix data  
- Economic impact evaluation based on fuel and electricity cost parameters  
- Scenario analysis:
  - Business-as-Usual  
  - Moderate Adoption  
  - Accelerated Adoption  

---

## Key Findings

- Electric Vehicle adoption significantly reduces CO₂ emissions compared to ICE vehicles  
- Environmental benefits depend on the electricity generation mix  
- EVs offer long-term economic advantages despite higher initial costs  
- Policy support and renewable energy integration enhance sustainability outcomes  

---

## Limitations and Future Work

- Battery lifecycle emissions are partially excluded  
- Regional infrastructure and behavioral factors are generalized  
- Charging infrastructure impacts are not explicitly modeled  

Future work will extend the model to include battery lifecycle analysis, grid load impacts, and country-level assessments.

---

## Authors / Team Members

**Chamali Abeysekara**  
BSc in Applied Data Science Communication  

**Team Members / Contributors:**  
- Rajintha Lakshani  
- Hussein Ziyard  
- Muhammed Nasir  

---
