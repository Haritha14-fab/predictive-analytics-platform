
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent

CLEAN_FILE = (
    BASE_DIR / "data" / "cleaned" / "online_retail_cleaned.csv"
)
MONTHLY_FILE = (
    BASE_DIR / "data" / "interim" / "monthly_sales.csv"
)
METRICS_FILE = (
    BASE_DIR / "outputs" / "reports" / "model_metrics.csv"
)
PRODUCT_FILE = (
    BASE_DIR / "outputs" / "reports" / "top_10_products.csv"
)
COUNTRY_FILE = (
    BASE_DIR / "outputs" / "reports" / "top_10_countries.csv"
)
FORECAST_FILE = (
    BASE_DIR / "outputs" / "forecasts" / "future_sales_forecast.csv"
)

st.set_page_config(
    page_title="Predictive Analytics Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Enterprise Predictive Analytics Platform")
st.caption("Historical Retail Sales Analysis & Forecasting")

# Load data
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

if not CLEAN_FILE.exists() or not MONTHLY_FILE.exists():
    st.error(
        "Required data files not found. "
        "Run data_ingestion.py, data_cleaning.py and "
        "prepare_timeseries.py first."
    )
    st.stop()

df = load_csv(CLEAN_FILE)
monthly = load_csv(MONTHLY_FILE)
monthly["Month"] = pd.to_datetime(monthly["Month"])

# Sidebar filters
st.sidebar.header("Dashboard Filters")

if "Country" in df.columns:
    countries = sorted(df["Country"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Select countries",
        countries,
        default=countries
    )
    filtered = df[df["Country"].isin(selected_countries)]
else:
    filtered = df.copy()

if filtered.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# KPI cards
filtered["Revenue"] = (
    filtered["Quantity"] * filtered["UnitPrice"]
)

total_revenue = filtered["Revenue"].sum()
total_orders = filtered["InvoiceNo"].nunique()
total_products = filtered["StockCode"].nunique()
total_customers = filtered["CustomerID"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"£{total_revenue:,.2f}")
c2.metric("Unique Invoices", f"{total_orders:,}")
c3.metric("Unique Products", f"{total_products:,}")
c4.metric("Unique Customers", f"{total_customers:,}")

st.divider()

# Historical sales trend
st.subheader("1. Monthly Historical Sales")

monthly_chart = px.line(
    monthly,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Revenue Trend"
)
monthly_chart.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (£)"
)
st.plotly_chart(monthly_chart, use_container_width=True)

# Product and country analysis
left, right = st.columns(2)

with left:
    st.subheader("2. Top Products by Revenue")

    if PRODUCT_FILE.exists():
        products = load_csv(PRODUCT_FILE)
        product_chart = px.bar(
            products.head(10),
            x="Revenue",
            y="Description",
            orientation="h",
            title="Top 10 Products"
        )
        product_chart.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )
        st.plotly_chart(product_chart, use_container_width=True)
    else:
        st.info("Run src/eda.py to generate the product report.")

with right:
    st.subheader("3. Top Countries by Revenue")

    if COUNTRY_FILE.exists():
        countries_df = load_csv(COUNTRY_FILE)
        country_chart = px.bar(
            countries_df.head(10),
            x="Country",
            y="Revenue",
            title="Top 10 Countries"
        )
        st.plotly_chart(country_chart, use_container_width=True)
    else:
        st.info("Run src/eda.py to generate the country report.")

# Model performance
st.divider()
st.subheader("4. Forecast Model Performance")

if METRICS_FILE.exists():
    metrics = load_csv(METRICS_FILE)
    st.dataframe(metrics, use_container_width=True)

    if {"Model", "MAE"}.issubset(metrics.columns):
        metric_chart = px.bar(
            metrics,
            x="Model",
            y="MAE",
            title="Model Comparison — MAE (Lower Is Better)"
        )
        st.plotly_chart(metric_chart, use_container_width=True)
else:
    st.info("Run src/forecast_model.py to generate model metrics.")

# Future forecast
st.subheader("5. Future Sales Forecast")

if FORECAST_FILE.exists():
    forecast = load_csv(FORECAST_FILE)
    st.dataframe(forecast, use_container_width=True)

    if {"Month", "Predicted_Sales"}.issubset(forecast.columns):
        forecast["Month"] = pd.to_datetime(forecast["Month"])
        forecast_chart = px.line(
            forecast,
            x="Month",
            y="Predicted_Sales",
            markers=True,
            title="Predicted Monthly Sales"
        )
        st.plotly_chart(forecast_chart, use_container_width=True)
else:
    st.info("Run src/future_forecast.py to generate forecasts.")

# Raw data preview
with st.expander("View cleaned transaction data"):
    st.dataframe(filtered.head(100), use_container_width=True)

st.caption(
    "Academic prototype. Forecasts are experimental because "
    "the dataset contains only 13 calendar months."
)
