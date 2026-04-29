# ----------------- IMPORTS -----------------
from http.client import GONE
import pandas as pd
import streamlit as st
import plotly.express as px

import analysis_codes as ac

st.markdown(
    """
    <style>
    .transparent-box {
        background-color: rgba(0, 0, 0, 0.6); /* Adjust alpha for transparency */
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 1);
        box-shadow: 0 4px 10px hex(0, 0, 0, 0);
    }
    .red {
        color: #ff4d4d; /* soft red */
        font-weight: bold;
    }
    .green {
        color: #32cd32; /* lime green */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- TAB FUNCTIONS -----------------
def home_tab():
    
    # Home tab content
    st.markdown("""
<h1 style="color:#FFD700; text-align:center; text-shadow:2px 2px 4px black;">
Global Model for Analyzing Environmental & Economic Impacts of EV Adoption
</h1>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="
    background-color: rgba(0, 0, 0, 0.6); 
    padding: 20px; 
    border-radius: 10px; 
    color: white; 
    font-size:18px;
">
The global adoption of Electric Vehicles (EVs) is accelerating as nations aim to reduce 
greenhouse gas (GHG) emissions and dependence on fossil fuels. EVs offer a sustainable 
alternative to traditional internal combustion engine (ICE) vehicles, with potential benefits 
including lower emissions, improved air quality, and long-term cost savings.

This portal showcases our research on the environmental and economic impacts of EV adoption worldwide. It includes:

- <b>Environmental Analysis:</b> Reduction of GHG emissions and cleaner energy solutions.<br>
- <b>Economic Analysis:</b> Cost of ownership, incentives, and market dynamics.<br>
- <b>Interactive Visuals:</b> Explore trends, regional comparisons, and projections.<br>

The goal is to provide insights for policymakers, researchers, and industry stakeholders 
to make informed decisions about the future of transportation.
</div>
""", unsafe_allow_html=True)
    
with st.container():
    # Title + body here


    # Background image CSS (applies when Home tab is active)
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("E:\Fourth sem\Rsearch Methods & Presentation\Project EV\Codes\jupyter\bg_img.jpeg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


def visuals_tab():
    st.title("EV Adoption & Impact Visuals")

    # ---------------- FIRST VISUAL ----------------

    st.markdown(
    """
    <div class="transparent-box">
        <h3>EV Growth Analysis 🚗⚡</h3>
        <p>This chart shows how the <strong>EV market share</strong> has grown over time in Norway.</p>
    </div>
    """,
    unsafe_allow_html=True
)
    fig = px.line(
        ac.yearly_summary,
        x="Year",
        y="EV_Share",
        markers=True,
        title="EV Share of Total Vehicles Over Time (Norway)",
        labels={"EV_Share": "EV Share (%)", "Year": "Year"}
    )

    fig.update_layout(
        xaxis=dict(range=[1990, 2026], showgrid=True),
        yaxis=dict(title="EV Share (%)"),
        template="plotly_white"
    )
    

    st.plotly_chart(fig, use_container_width=True)
    # ---------------- SECOND VISUAL ----------------
    st.markdown('''
    <div class="transparent-box">
        <h3>EV vs ICE Registrations in Norway 🚗⚡⛽</h3>
        <p>This chart compares how EVs and ICE vehicles have trended over time.</p>
    </div>
    ''', unsafe_allow_html=True)
    # Reshape the data for Plotly (long format is better for multiple lines)
    df_long = ac.yearly_summary.melt(
        id_vars="Year",
        value_vars=["EV_Total", "ICE_Total"],
        var_name="Vehicle_Type",
        value_name="Registrations"
    )

    fig = px.line(
        df_long,
        x="Year",
        y="Registrations",
        color="Vehicle_Type",
        markers=True,
        title="EV vs ICE Registrations in Norway",
        labels={
            "Year": "Year",
            "Registrations": "Number of Vehicles",
            "Vehicle_Type": "Type"
        }
    )

    fig.update_layout(
        xaxis=dict(range=[1990, 2026], showgrid=True),
        yaxis=dict(title="Number of Vehicles"),
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
    # --- Run calculations ---
    yearly_summary, totals = ac.calculate_impacts(ac.yearly_summary)

    # --- Year filter ---
    years = yearly_summary['Year'].unique()
    selected_years = st.multiselect("Select Year(s) to view", options=years, default=years)

    # Filter data
    filtered_data = yearly_summary[yearly_summary['Year'].isin(selected_years)]

    # Recalculate totals for filtered years
    filtered_totals = {
        "ev_total": int(filtered_data["EV_Total"].sum()),
        "ice_total": int(filtered_data["ICE_Total"].sum()),
        "ev_energy": int(filtered_data["EV_Energy_Demand_kWh"].sum()),
        "ice_fuel": int(filtered_data["ICE_Fuel_Demand_L"].sum()),
        "ice_co2_kg": int(filtered_data["ICE_CO2_Emissions_kg"].sum()),
        "ice_co2_tonnes": int(filtered_data["ICE_CO2_Emissions_tonnes"].sum()),
        "net_co2_savings": int(filtered_data["Net_CO2_Savings_kg"].sum())
    }

    # --- Display HTML summary ---
    st.markdown(f"""
    <div class="transparent-box">
        <h4>EV & ICE Summary 📊</h4>
        <ul>
            <li><strong>Total EV Registrations:</strong><span class="green"> {filtered_totals['ev_total']}</span></li>
            <li><strong>Total ICE Registrations:</strong><span class="red"> {filtered_totals['ice_total']}</span></li>
            <li><strong>Total EV Energy Demand (kWh):</strong><span class="green"> {filtered_totals['ev_energy']}</span></li>
            <li><strong>Total ICE Fuel Demand (L):</strong><span class="red"> {filtered_totals['ice_fuel']}</span></li>
            <li><strong>Total ICE CO₂ Emissions (kg):</strong><span class="red"> {filtered_totals['ice_co2_kg']}</span></li>
            <li><strong>Total ICE CO₂ Emissions (tonnes):</strong><span class="red"> {filtered_totals['ice_co2_tonnes']}</span></li>
            <li><strong>Net CO₂ Savings (kg):</strong><span class="green"> {filtered_totals['net_co2_savings']}</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # --- Plot: Energy Demand ---
    import matplotlib.pyplot as plt

    st.write("### Energy Demand: EV vs ICE")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot lines
    ax.plot(filtered_data["Year"], filtered_data["EV_Energy_Demand_kWh"], label="EV Energy Demand (kWh)", marker="o")
    ax.plot(filtered_data["Year"], filtered_data["ICE_Fuel_Demand_L"], label="ICE Fuel Demand (Litres)", marker="s")

    # Labels and title
    ax.set_xlabel("Year")
    ax.set_ylabel("Demand")
    ax.set_title("Energy Demand: EV vs ICE")
    ax.set_xlim(filtered_data["Year"].min(), filtered_data["Year"].max())
    ax.legend()

# Show figure in Streamlit
    st.pyplot(fig)

    # ---------------- THIRD VISUAL ----------------
    

    # ---- HEADER ----
    st.markdown("""
    <div class="transparent-box">
    <h1>⚡ Energy Demand Analysis: EV vs ICE</h1>

    <p>This chart compares the yearly <strong>energy demand</strong> of Electric Vehicles (EVs)
    and Internal Combustion Engine (ICE) vehicles.</p>

    <ul>
        <li><strong>EV Energy Demand</strong> is measured in <em>kWh</em>.</li>
        <li><strong>ICE Fuel Demand</strong> is measured in <em>litres</em>.</li>
    </ul>
    <div id="chart"></div>
    """, unsafe_allow_html=True)


    # ---- INTERACTIVE PLOT ----
    fig = px.line(
    ac.yearly_summary,
    x="Year",
    y=["EV_Energy_Demand_kWh", "ICE_Fuel_Demand_L"],
    labels={"value": "Demand", "Year": "Year"},
    title="Energy Demand: EV vs ICE",
    markers=True
)

    # Customize legend names
    fig.for_each_trace(lambda t: t.update(name={
    "EV_Energy_Demand_kWh": "EV Energy Demand (kWh)",
    "ICE_Fuel_Demand_L": "ICE Fuel Demand (Litres)"
    }[t.name]))

    # Show in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- FOURTH VISUAL ----------------
    # ---- HEADER ----
    st.markdown(
        """ 
    <div class="transparent-box">
    <h1>ICE Vehicle CO₂ Emissions Over Time</h1>
   
    <h3>
    This chart shows the yearly CO₂ emissions from Internal Combustion Engine (ICE) vehicles.  
    - ICE CO₂ Emissions are measured in tonnes.  
    </h3>
    </div>
""", unsafe_allow_html=True)


# ---- INTERACTIVE BAR CHART ----
    fig = px.bar(
    ac.yearly_summary,
    x="Year",
    y="ICE_CO2_Emissions_tonnes",
    labels={"ICE_CO2_Emissions_tonnes": "CO₂ Emissions (tonnes)", "Year": "Year"},
    title="ICE Vehicle CO₂ Emissions Over Time",
    color_discrete_sequence=["red"]
)

# Customize layout
    fig.update_layout(
    xaxis=dict(range=[1990, 2026], title="Year"),
    yaxis=dict(title="CO₂ Emissions (tonnes)"),
    template="plotly_white"
)

# Show in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Yearly Energy Generation by Source")
    st.dataframe(ac.energy_by_year)

    for i, row in ac.summary.iterrows():
        st.write(f"{row['Energy_Category']}: {row['Value']}")

    fig = px.bar(ac.energy_by_year, 
             x='Year', 
             y=ac.energy_by_year.columns[1:],  # skip 'Year'
             title='Yearly Energy Generation by Source',
             labels={'value':'Energy Value', 'variable':'Energy Source'},
             barmode='stack')
    st.plotly_chart(fig)

    fig = px.pie(ac.summary, names='Energy_Category', values='Value',
             title='Energy Generation Share by Category')
    st.plotly_chart(fig)

    fig = px.line(ac.energy_by_year, x='Year', y=ac.energy_by_year.columns[1:],
              title='Energy Generation Trend by Source',
              labels={'value':'Energy Value', 'variable':'Energy Source'})
    st.plotly_chart(fig)

    fig = px.treemap(ac.energy_df, path=['Energy_Category', 'Variable'], values='Value',
                 title='Energy Generation Hierarchy')
    st.plotly_chart(fig)

    
    # ---------------- PLACEHOLDER FOR MORE VISUALS ----------------
    st.markdown("🚧 More visualizations will be added here soon...")

# ----------------- MAIN APP -----------------
tab = st.sidebar.selectbox("Choose a tab", ["Home", "Visuals"])

if tab == "Home":
    home_tab()
elif tab == "Visuals":
    visuals_tab()

def run_portal():
    return f"Running portal..."
