
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "online_retail_raw.csv"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
REPORT_DIR = BASE_DIR / "outputs" / "reports"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = CLEAN_DIR / "online_retail_cleaned.csv"

print("=" * 55)
print("STEP 4: DATA CLEANING")
print("=" * 55)

# Load raw dataset
df = pd.read_csv(RAW_FILE)

print("\nOriginal rows:", len(df))

# 1. Convert columns to correct data types
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)

df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)

df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"], errors="coerce"
)

# 2. Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print("Duplicate rows removed:", before - len(df))

# 3. Remove rows with missing essential product/date information
before = len(df)
df = df.dropna(subset=["InvoiceDate", "Description"])
print("Rows removed for missing date/description:", before - len(df))

# 4. Remove invalid quantities and prices
before = len(df)
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
print("Rows removed for invalid quantity/price:", before - len(df))

# 5. Keep CustomerID missing values for now.
# They may still be useful for overall sales analysis.
# Customer-level analysis will handle missing IDs separately.

# 6. Create a revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# 7. Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned rows:", len(df))
print("Cleaned columns:", df.columns.tolist())
print("Remaining missing values:")
print(df.isnull().sum())

print("\nCleaned dataset saved to:")
print(OUTPUT_FILE)

# Save a simple cleaning summary
summary = pd.DataFrame({
    "Metric": [
        "Original rows",
        "Cleaned rows",
        "Rows removed",
        "Remaining duplicate rows"
    ],
    "Value": [
        541909,
        len(df),
        541909 - len(df),
        int(df.duplicated().sum())
    ]
})

summary.to_csv(
    REPORT_DIR / "data_cleaning_summary.csv",
    index=False
)

print("\nCleaning summary saved.")
print("DATA CLEANING COMPLETED")
