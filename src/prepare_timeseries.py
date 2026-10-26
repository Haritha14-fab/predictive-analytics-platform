
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "cleaned" / "online_retail_cleaned.csv"
)
OUTPUT_DIR = BASE_DIR / "data" / "interim"
REPORT_DIR = BASE_DIR / "outputs" / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "monthly_sales.csv"

print("=" * 55)
print("STEP 6: TIME-SERIES DATA PREPARATION")
print("=" * 55)

df = pd.read_csv(INPUT_FILE, parse_dates=["InvoiceDate"])

# Ensure revenue is calculated
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Aggregate transaction revenue by month
df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = (
    df.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
    .to_frame()
)

# Fill missing calendar months with zero sales
full_months = pd.period_range(
    start=monthly_sales.index.min(),
    end=monthly_sales.index.max(),
    freq="M"
)

monthly_sales = monthly_sales.reindex(full_months, fill_value=0)
monthly_sales.index.name = "Month"
monthly_sales = monthly_sales.reset_index()

monthly_sales["Month"] = monthly_sales["Month"].astype(str)
monthly_sales = monthly_sales.rename(
    columns={"Revenue": "Sales"}
)

monthly_sales.to_csv(OUTPUT_FILE, index=False)

print("\nMonthly dataset shape:", monthly_sales.shape)
print("\nFirst 5 rows:")
print(monthly_sales.head())

print("\nLast 5 rows:")
print(monthly_sales.tail())

print("\nDate range:",
      monthly_sales["Month"].min(),
      "to",
      monthly_sales["Month"].max())

print("\nSaved monthly time-series data to:")
print(OUTPUT_FILE)

print("\nTIME-SERIES PREPARATION COMPLETED")
