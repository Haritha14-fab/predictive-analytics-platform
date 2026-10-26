
from pathlib import Path
import pandas as pd
from ucimlrepo import fetch_ucirepo

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = RAW_DIR / "online_retail_raw.csv"

print("=" * 50)
print("PREDICTIVE ANALYTICS PROJECT")
print("STEP 2: DATA INGESTION")
print("=" * 50)

# Fetch dataset directly from UCI
online_retail = fetch_ucirepo(id=352)

# Use original data to include ID columns too
df = online_retail.data.original.copy()

print("\nDataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst five rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

# Save dataset to project folder
df.to_csv(OUTPUT_FILE, index=False)

print("\nDataset saved successfully!")
print(OUTPUT_FILE)

# Verify expected columns
required_columns = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if not missing_columns:
    print("\nSUCCESS: All 8 expected columns are present.")
else:
    print("\nMissing columns:", missing_columns)

# Save dataset information
print("\nUCI Dataset:", online_retail.metadata.name)
print("Dataset ID:", online_retail.metadata.uci_id)
