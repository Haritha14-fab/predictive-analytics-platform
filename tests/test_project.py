
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


def test_cleaned_dataset_exists():
    path = BASE_DIR / "data" / "cleaned" / "online_retail_cleaned.csv"
    assert path.exists(), "Run src/data_cleaning.py first"


def test_cleaned_dataset_has_required_columns():
    path = BASE_DIR / "data" / "cleaned" / "online_retail_cleaned.csv"
    df = pd.read_csv(path, nrows=5)

    required = {
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country",
        "Revenue"
    }

    assert required.issubset(set(df.columns))


def test_revenue_calculation():
    quantity = 3
    unit_price = 2.50
    revenue = quantity * unit_price

    assert revenue == 7.50


def test_cleaned_data_has_valid_sales():
    path = BASE_DIR / "data" / "cleaned" / "online_retail_cleaned.csv"
    df = pd.read_csv(path, usecols=["Quantity", "UnitPrice"], nrows=1000)

    assert (df["Quantity"] > 0).all()
    assert (df["UnitPrice"] > 0).all()


def test_monthly_sales_file_exists():
    path = BASE_DIR / "data" / "interim" / "monthly_sales.csv"
    assert path.exists(), "Run src/prepare_timeseries.py first"

    df = pd.read_csv(path)
    assert {"Month", "Sales"}.issubset(set(df.columns))
    assert len(df) > 0
