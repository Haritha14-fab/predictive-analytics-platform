
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "cleaned" / "online_retail_cleaned.csv"
FIGURE_DIR = BASE_DIR / "outputs" / "figures"
REPORT_DIR = BASE_DIR / "outputs" / "reports"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

print("=" * 55)
print("STEP 5: EXPLORATORY DATA ANALYSIS")
print("=" * 55)

df = pd.read_csv(DATA_FILE, parse_dates=["InvoiceDate"])

# Ensure revenue exists
if "Revenue" not in df.columns:
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# 1. Overall business summary
summary = {
    "Total Transactions (Rows)": len(df),
    "Total Revenue": round(df["Revenue"].sum(), 2),
    "Unique Invoices": df["InvoiceNo"].nunique(),
    "Unique Products": df["StockCode"].nunique(),
    "Unique Countries": df["Country"].nunique(),
    "Unique Customers": df["CustomerID"].nunique()
}

print("\n1. BUSINESS SUMMARY")
for key, value in summary.items():
    print(f"{key}: {value}")

pd.DataFrame(
    summary.items(), columns=["Metric", "Value"]
).to_csv(REPORT_DIR / "business_summary.csv", index=False)

# 2. Monthly revenue trend
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

monthly = (
    df.groupby("Month", as_index=False)["Revenue"]
    .sum()
    .sort_values("Month")
)

plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly, x="Month", y="Revenue", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIGURE_DIR / "monthly_revenue_trend.png", dpi=150)
plt.close()

monthly.to_csv(REPORT_DIR / "monthly_revenue.csv", index=False)

# 3. Top 10 products by revenue
products = (
    df.groupby("Description", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 7))
sns.barplot(data=products, x="Revenue", y="Description")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(FIGURE_DIR / "top_10_products.png", dpi=150)
plt.close()

products.to_csv(REPORT_DIR / "top_10_products.csv", index=False)

# 4. Top 10 countries by revenue
countries = (
    df.groupby("Country", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 7))
sns.barplot(data=countries, x="Revenue", y="Country")
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig(FIGURE_DIR / "top_10_countries.png", dpi=150)
plt.close()

countries.to_csv(REPORT_DIR / "top_10_countries.csv", index=False)

print("\nCharts saved in:", FIGURE_DIR)
print("Reports saved in:", REPORT_DIR)
print("\nEDA COMPLETED SUCCESSFULLY")
