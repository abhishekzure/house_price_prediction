from pathlib import Path

import joblib
import pandas as pd
from django.conf import settings


MODEL_PATH = (
    Path(settings.BASE_DIR)
    / "model"
    / "house_price_predict.pkl"
)


def predict_house_price(data):
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model missing. Run python train.py first."
        )

    loaded = joblib.load(MODEL_PATH)
    if isinstance(loaded, dict) and "model" in loaded:
        model = loaded["model"]
        feature_order = loaded.get("features")
    else:
        model = loaded
        feature_order = None

    parking_val = 1 if str(data.get("parking", "0")).strip() in ["1", "Yes", "True"] else 0
    lift_val = 1 if str(data.get("lift", "0")).strip() in ["1", "Yes", "True"] else 0
    gated_val = 1 if str(data.get("gated_society", "0")).strip() in ["1", "Yes", "True"] else 0

    features = pd.DataFrame([{
        "City": str(data["city"]).strip(),
        "Locality_Tier": str(data["locality_tier"]).strip(),
        "BHK": int(data["bhk"]),
        "Bathrooms": int(data["bathrooms"]),
        "Super_Area_sqft": float(data["super_area_sqft"]),
        "Carpet_Area_sqft": float(data.get("carpet_area_sqft") or data["super_area_sqft"]),
        "Floor_No": int(data["floor_no"]),
        "Total_Floors": int(data.get("total_floors") or 10),
        "Property_Age_years": int(data["property_age_years"]),
        "Parking": parking_val,
        "Furnishing": str(data["furnishing"]).strip(),
        "Lift": lift_val,
        "Gated_Society": gated_val,
        "Distance_to_Metro_km": float(data["distance_to_metro_km"]),
        "Distance_to_CityCenter_km": float(data["distance_to_citycenter_km"]),
        "Nearby_School_km": float(data["nearby_school_km"]),
        "Nearby_Hospital_km": float(data["nearby_hospital_km"]),
        "Crime_Rate_Index": float(data["crime_rate_index"]),
    }])

    if feature_order:
        input_encoded = pd.get_dummies(features, dummy_na=True)
        input_encoded = input_encoded.reindex(columns=feature_order, fill_value=0)
        price = float(model.predict(input_encoded)[0])
    else:
        price = float(model.predict(features)[0])

    price = max(0.0, price)

    if not pd.notna(price):
        raise ValueError("The model returned an invalid price.")

    return round(price, 2)
