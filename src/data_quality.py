
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw" / "online_retail_raw.csv"
REPORT_DIR = BASE_DIR / "outputs" / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 50)
print("STEP 3: DATA QUALITY AUDIT")
print("=" * 50)

df = pd.read_csv(RAW_FILE)

# 1. Dataset size
print("\n1. Dataset shape:", df.shape)

# 2. Column names and data types
print("\n2. Column names:")
print(df.columns.tolist())

print("\n3. Data types:")
print(df.dtypes)

# 3. Missing values
print("\n4. Missing values:")
missing = df.isnull().sum()
print(missing[missing > 0])

# 4. Duplicate records
duplicates = df.duplicated().sum()
print("\n5. Duplicate rows:", duplicates)

# 5. Invalid quantities and prices
print("\n6. Zero or negative quantities:",
      (df["Quantity"] <= 0).sum())

print("Zero or negative unit prices:",
      (df["UnitPrice"] <= 0).sum())

# 6. Cancelled invoices
cancelled = (
    df["InvoiceNo"].astype(str).str.startswith("C", na=False)
).sum()

print("\n7. Cancelled invoice rows:", cancelled)

# 7. Save audit report
report = pd.DataFrame({
    "MissingValues": df.isnull().sum(),
    "DataType": df.dtypes.astype(str)
})

report.to_csv(REPORT_DIR / "data_quality_report.csv")

print("\nAudit report saved to:")
print(REPORT_DIR / "data_quality_report.csv")

print("\nDATA QUALITY AUDIT COMPLETED")
