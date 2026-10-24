import pandas as pd
import joblib
import json
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# 1. Set file paths
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "model"

DATASET_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

# 2. Load dataset
df = pd.read_csv(DATASET_DIR / "house_price_predict.csv")

# 3. Clean column names and missing values
df.columns = df.columns.str.strip()
df = df.dropna(subset=["Market_Price_INR"])

# 4. Select input features
numeric_features = [
    "BHK",
    "Bathrooms",
    "Super_Area_sqft",
    "Carpet_Area_sqft",
    "Floor_No",
    "Total_Floors",
    "Property_Age_years",
    "Distance_to_Metro_km",
    "Distance_to_CityCenter_km",
    "Nearby_School_km",
    "Nearby_Hospital_km",
    "Crime_Rate_Index"
]

categorical_features = [
    "City",
    "Locality_Tier",
    "Furnishing",
    "Parking",
    "Lift",
    "Gated_Society"
]

features = numeric_features + categorical_features
target = "Market_Price_INR"

# Convert target to numbers
df[target] = pd.to_numeric(
    df[target].astype(str).str.replace(",", "").str.replace("₹", ""),
    errors="coerce"
)
df = df.dropna(subset=[target])

# Strip whitespace from string categories
for col in categorical_features:
    if col in df.columns and (df[col].dtype == object or str(df[col].dtype).startswith("str")):
        df[col] = df[col].astype(str).str.strip()

# Convert categorical columns into numeric columns
X = pd.get_dummies(df[features], dummy_na=True)
y = df[target]

# 5. Split dataset: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# Save training and testing datasets
train_df = X_train.copy()
train_df[target] = y_train
train_df.to_csv(DATASET_DIR / "train.csv", index=False)

test_df = X_test.copy()
test_df[target] = y_test
test_df.to_csv(DATASET_DIR / "test.csv", index=False)

# 6. Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# 7. Test the model
predictions = model.predict(X_test)

r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5

print("Model Training Completed!")
print("R2 Score:", round(r2, 4))
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))

# 8. Save the trained model and its feature columns
bundle = {"model": model, "features": list(X.columns)}
joblib.dump(bundle, MODEL_DIR / "house_price_predict.pkl")
joblib.dump(bundle, MODEL_DIR / "house_price_model.pkl")
joblib.dump(bundle, MODEL_DIR / "house_price_model.joblib")

# 9. Save model performance metrics
metrics = {
    "selected_model": "Linear Regression",
    "metrics": {
        "Linear Regression": {
            "r2": round(r2, 4),
            "mae_inr": round(mae, 2),
            "mse": round(mse, 2),
            "rmse": round(rmse, 2)
        }
    }
}

with open(MODEL_DIR / "model_metrics.json", "w") as file:
    json.dump(metrics, file, indent=4)

print("Model and metrics saved successfully!")
