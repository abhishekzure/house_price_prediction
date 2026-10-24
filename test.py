import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# 1. Set file paths
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "model"

# 2. Load the trained model and feature columns
bundle = joblib.load(MODEL_DIR / "house_price_predict.pkl")
model = bundle["model"]
features = bundle["features"]

# 3. Load the test dataset
test_df = pd.read_csv(DATASET_DIR / "test.csv")
target = "Market_Price_INR"

X_test = test_df[features]
y_test = test_df[target]

# 4. Predict house prices on test data
predictions = model.predict(X_test)

# 5. Evaluate the model performance
r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5

print("=" * 50)
print("       TEST MODEL EVALUATION RESULTS")
print("=" * 50)
print("Total Test Samples:", len(y_test))
print("R2 Score (Accuracy):", round(r2, 4))
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("=" * 50)

# 6. Display sample predictions (Actual vs Predicted)
results = pd.DataFrame({
    "Actual Price (INR)": y_test.values[:5],
    "Predicted Price (INR)": predictions[:5].round(2)
})
results["Difference"] = (results["Actual Price (INR)"] - results["Predicted Price (INR)"]).abs().round(2)

print("\nSample Test Predictions (First 5 records):")
print(results)
