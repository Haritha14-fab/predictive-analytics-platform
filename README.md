
# Enterprise Predictive Analytics & Demand Forecasting Platform

## Overview

A Python-based retail analytics project that analyzes historical
Online Retail transaction data, identifies sales patterns, evaluates
forecasting models, and displays insights in an interactive Streamlit
dashboard.

## Features

- Automated dataset ingestion using the UCI repository
- Data quality audit and cleaning
- Revenue calculation and monthly sales aggregation
- Exploratory data analysis
- Product and country revenue analysis
- Time-series feature engineering
- Chronological model evaluation using MAE and RMSE
- Experimental future sales forecasting
- Interactive Streamlit dashboard
- Automated tests with pytest

## Tech Stack

- Python
- Pandas and NumPy
- Scikit-learn
- Matplotlib and Seaborn
- Streamlit and Plotly
- Pytest
- UCI Online Retail dataset

## Project Structure

```text
predictive-analytics-platform/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── interim/
├── src/
│   ├── data_ingestion.py
│   ├── data_quality.py
│   ├── data_cleaning.py
│   ├── eda.py
│   ├── prepare_timeseries.py
│   ├── forecast_model.py
│   ├── evaluate_model.py
│   └── future_forecast.py
├── outputs/
│   ├── figures/
│   ├── reports/
│   └── forecasts/
└── tests/
    └── test_project.py
```

## Setup

Install Python 3.10 or newer.

```bash
python -m pip install -r requirements.txt
```

## Run the Pipeline

Run these commands from the project root:

```bash
python src/data_ingestion.py
python src/data_quality.py
python src/data_cleaning.py
python src/eda.py
python src/prepare_timeseries.py
python src/forecast_model.py
python src/evaluate_model.py
python src/future_forecast.py
```

## Launch Dashboard

```bash
python -m streamlit run app.py
```

## Run Tests

```bash
python -m pytest -v
```

## Dataset

UCI Machine Learning Repository — Online Retail:

https://archive.ics.uci.edu/dataset/352/online+retail

## Limitations

The current dataset covers approximately 13 calendar months.
Forecasts are experimental and should not be interpreted as reliable
long-term business predictions. More historical data and stronger
time-series validation are required.

## Disclaimer

This is an academic portfolio project. Forecasts are estimates and
are not guaranteed to represent future business performance.
