
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

PREDICTIONS_FILE = (
    BASE_DIR / "outputs" / "forecasts" / "test_predictions.csv"
)
FIGURE_DIR = BASE_DIR / "outputs" / "figures"
REPORT_DIR = BASE_DIR / "outputs" / "reports"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 55)
print("STEP 8: MODEL EVALUATION AND VISUALIZATION")
print("=" * 55)

df = pd.read_csv(PREDICTIONS_FILE)

df["Month"] = pd.to_datetime(df["Month"])

print("\nTest predictions:")
print(df.to_string(index=False))

# Plot actual sales against model predictions
plt.figure(figsize=(11, 6))

plt.plot(
    df["Month"], df["Actual_Sales"],
    marker="o", label="Actual Sales"
)

plt.plot(
    df["Month"], df["Model_Prediction"],
    marker="s", linestyle="--", label="Predicted Sales"
)

plt.title("Actual vs Predicted Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

chart_file = FIGURE_DIR / "actual_vs_predicted_sales.png"
plt.savefig(chart_file, dpi=150)
plt.close()

# Calculate prediction error for each test month
df["Prediction_Error"] = (
    df["Actual_Sales"] - df["Model_Prediction"]
)

df["Absolute_Error"] = df["Prediction_Error"].abs()

error_file = REPORT_DIR / "prediction_errors.csv"
df.to_csv(error_file, index=False)

print("\nChart saved to:", chart_file)
print("Prediction error report saved to:", error_file)
print("\nEVALUATION VISUALIZATION COMPLETED")
