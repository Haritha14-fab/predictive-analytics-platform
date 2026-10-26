
from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "interim" / "monthly_sales.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "forecasts"
REPORT_DIR = BASE_DIR / "outputs" / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 55)
print("STEP 7: SALES FORECASTING MODEL")
print("=" * 55)

df = pd.read_csv(
    INPUT_FILE,
    dtype={"Month": str},
    low_memory=False
)

df["Month"] = pd.to_datetime(df["Month"])
df = df.sort_values("Month").reset_index(drop=True)

if len(df) < 8:
    raise ValueError("At least 8 monthly observations are needed.")

# Build features using only past sales
df["lag_1"] = df["Sales"].shift(1)
df["lag_2"] = df["Sales"].shift(2)
df["lag_3"] = df["Sales"].shift(3)
df["rolling_mean_3"] = df["Sales"].shift(1).rolling(3).mean()
df["month_number"] = df["Month"].dt.month
df["time_index"] = np.arange(len(df))

df = df.dropna().reset_index(drop=True)

features = [
    "lag_1", "lag_2", "lag_3",
    "rolling_mean_3", "month_number", "time_index"
]

X = df[features]
y = df["Sales"]

# Reserve the latest 3 usable months for testing
test_size = 3
split_index = len(df) - test_size

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]
y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

if len(X_train) < 3:
    raise ValueError("Too few training observations after feature creation.")

# Baseline: predict the previous month's sales
baseline = X_test["lag_1"].to_numpy()

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=3,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

def calculate_metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    return mae, rmse

baseline_mae, baseline_rmse = calculate_metrics(y_test, baseline)
model_mae, model_rmse = calculate_metrics(y_test, predictions)

print("\nTotal monthly observations:", len(df))
print("Training observations:", len(X_train))
print("Testing observations:", len(X_test))

print("\nBaseline MAE:", round(baseline_mae, 2))
print("Baseline RMSE:", round(baseline_rmse, 2))
print("\nRandom Forest MAE:", round(model_mae, 2))
print("Random Forest RMSE:", round(model_rmse, 2))

results = pd.DataFrame({
    "Month": df.loc[X_test.index, "Month"].dt.strftime("%Y-%m").to_numpy(),
    "Actual_Sales": y_test.to_numpy(),
    "Baseline_Prediction": baseline,
    "Model_Prediction": predictions
})

results.to_csv(OUTPUT_DIR / "test_predictions.csv", index=False)

metrics = pd.DataFrame([
    {"Model": "Previous Month Baseline",
     "MAE": baseline_mae, "RMSE": baseline_rmse},
    {"Model": "Random Forest",
     "MAE": model_mae, "RMSE": model_rmse}
])

metrics.to_csv(REPORT_DIR / "model_metrics.csv", index=False)

print("\nPredictions saved to:", OUTPUT_DIR / "test_predictions.csv")
print("Metrics saved to:", REPORT_DIR / "model_metrics.csv")
print("\nMODEL TRAINING COMPLETED")
print("Note: Results are preliminary because only 13 calendar months are available.")
