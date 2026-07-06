import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(str(Path(__file__).resolve().parents[1]))
import config
from src.analytics_engine import CreditPortfolioAnalyticsEngine

st.set_page_config(page_title="Institutional Portfolio Cockpit", layout="wide")
st.title("Institutional Credit Risk & Portfolio Analytics Cockpit")
st.markdown("---")

# Load analytical data matrices
analyzer = CreditPortfolioAnalyticsEngine()
try:
    df_raw = analyzer.load_portfolio_dataframe()
    df_portfolio = analyzer.compute_portfolio_metrics(df_raw)
except Exception:
    st.error("CRITICAL ERROR: Unable to parse relational credit assets database. Ensure database and seed arrays are executed.")
    st.stop()

# Interactive Stress Testing Adjustments
st.sidebar.header("Macroeconomic Stress-Test Shocks")
pd_multiplier = st.sidebar.slider("Systemic PD Multiplier (Credit Deterioration)", 1.0, 3.0, 1.0, step=0.1)
lgd_multiplier = st.sidebar.slider("Property/Collateral Haircut (LGD Multiplier)", 1.0, 2.0, 1.0, step=0.1)

# Apply Shocks on the fly
df_portfolio["probability_of_default"] = (df_portfolio["probability_of_default"] * pd_multiplier).clip(upper=0.99)
df_portfolio["loss_given_default"] = (df_portfolio["loss_given_default"] * lgd_multiplier).clip(upper=0.99)
# Re-evaluate expected losses post shock applications
df_portfolio["Expected_Loss"] = df_portfolio["probability_of_default"] * df_portfolio["loss_given_default"] * df_portfolio["EAD"]

# Key Performance Indicators Row
tot_ead = df_portfolio["EAD"].sum()
tot_el = df_portfolio["Expected_Loss"].sum()
weighted_pd = (df_portfolio["probability_of_default"] * df_portfolio["EAD"]).sum() / tot_ead
weighted_lgd = (df_portfolio["loss_given_default"] * df_portfolio["EAD"]).sum() / tot_ead

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Portfolio Total EAD", f"${tot_ead:,.0f}")
kpi2.metric("Total Portfolio Expected Loss (EL)", f"${tot_el:,.0f}", delta=f"${tot_el - (tot_el/pd_multiplier/lgd_multiplier):,.0f} Shock Increase", delta_color="inverse")
kpi3.metric("Portfolio Weighted PD", f"{weighted_pd * 100:.2f}%")
kpi4.metric("Portfolio Weighted LGD", f"{weighted_lgd * 100:.2f}%")

st.markdown("---")

# Visualization Layout Components
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Concentration of Risk Exposure Across Operational Sectors")
    fig_pie = px.pie(df_portfolio, values="EAD", names="segment", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("Expected Loss vs. Exposure Profile Breakdown")
    fig_bar = px.bar(
        df_portfolio.groupby("segment")[["EAD", "Expected_Loss"]].sum().reset_index(),
        x="segment", y="Expected_Loss", text_auto=".2s",
        title="Aggregate Sector Specific Expected Losses",
        color_discrete_sequence=["#EF553B"]
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Granular Data Subsets Tables View
st.subheader("Core Structured Portfolio Credit Assets Query Table")
st.dataframe(
    df_portfolio[["facility_id", "borrower_name", "segment", "committed_exposure", "EAD", "probability_of_default", "loss_given_default", "Expected_Loss"]]
    .style.format({
        "committed_exposure": "${:,.0f}", "EAD": "${:,.0f}",
        "probability_of_default": "{:.2%}", "loss_given_default": "{:.2%}", "Expected_Loss": "${:,.2f}"
    }),
    use_container_width=True
)