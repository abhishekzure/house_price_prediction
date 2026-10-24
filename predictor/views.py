import json
from pathlib import Path

import joblib
import pandas as pd

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import HousePredictionForm
from .models import Prediction
from .reports import generate_single_prediction_pdf


MODEL_DIR = Path(settings.BASE_DIR) / "model"
BUNDLE_PATH = MODEL_DIR / "house_price_predict.pkl"
METRICS_PATH = MODEL_DIR / "model_metrics.json"

_cached_bundle = None


def load_model_bundle():
    global _cached_bundle
    if _cached_bundle is not None:
        return _cached_bundle

    # Determine default model name from metrics if available
    selected_name = "Linear Regression"
    if METRICS_PATH.exists():
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                selected_name = json.load(f).get("selected_model", "Linear Regression")
        except Exception:
            pass

    for path in [
        MODEL_DIR / "house_price_predict.pkl",
        MODEL_DIR / "house_price_model.pkl",
        MODEL_DIR / "house_price_model.joblib",
    ]:
        if path.exists():
            loaded = joblib.load(path)
            if isinstance(loaded, dict) and "model" in loaded:
                model_obj = loaded["model"]
                feature_cols = loaded.get("features", [])
            else:
                model_obj = loaded
                feature_cols = None

            _cached_bundle = {
                "models": {
                    selected_name: model_obj,
                    "Linear Regression": model_obj,
                    "Random Forest": model_obj,
                },
                "selected_model": selected_name,
                "features": feature_cols,
            }
            return _cached_bundle

    raise FileNotFoundError(
        "Trained models not found. "
        "Run: python train.py"
    )


def load_metrics():
    if not METRICS_PATH.exists():
        raise FileNotFoundError(
            "Model metrics not found. "
            "Run: python train.py"
        )

    with open(
        METRICS_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def index(request):
    metrics_report = None
    r2_score_val = None
    mae_val = None
    try:
        metrics_report = load_metrics()
        if metrics_report and "metrics" in metrics_report:
            model_name = metrics_report.get("selected_model", "Linear Regression")
            model_data = (
                metrics_report["metrics"].get(model_name)
                or metrics_report["metrics"].get("Linear Regression")
                or metrics_report["metrics"].get("Random Forest")
                or {}
            )
            r2_score_val = model_data.get("r2")
            mae_val = model_data.get("mae_inr")
    except (FileNotFoundError, json.JSONDecodeError):
        metrics_report = None

    total_predictions = Prediction.objects.count()
    recent_predictions = (
        Prediction.objects.select_related("user")
        .order_by("-created_at")[:5]
    )

    context = {
        "metrics_report": metrics_report,
        "r2_score": r2_score_val,
        "mae": mae_val,
        "total_predictions": total_predictions,
        "recent_predictions": recent_predictions,
    }
    return render(request, "index.html", context)


@login_required
def predict_price(request):
    result = None
    error_message = None
    form = HousePredictionForm(request.POST or None)
    metrics_report = None

    try:
        metrics_report = load_metrics()
    except (FileNotFoundError, json.JSONDecodeError):
        error_message = (
            "Model metrics are unavailable. "
            "Train the models before making predictions."
        )

    if request.method == "POST" and form.is_valid():
        try:
            bundle = load_model_bundle()

            selected_model = bundle.get("selected_model", "Linear Regression")
            model = bundle["models"].get(selected_model) or list(bundle["models"].values())[0]
            feature_cols = bundle.get("features")

            parking_val = 1 if form.cleaned_data["Parking"] in ["Yes", 1, "1", True] else 0
            lift_val = 1 if form.cleaned_data["Lift"] in ["Yes", 1, "1", True] else 0
            gated_val = 1 if form.cleaned_data["Gated_Society"] in ["Yes", 1, "1", True] else 0

            input_data = pd.DataFrame([{
                "BHK": form.cleaned_data["BHK"],
                "Bathrooms": form.cleaned_data["Bathrooms"],
                "Super_Area_sqft": form.cleaned_data["Super_Area_sqft"],
                "Carpet_Area_sqft": form.cleaned_data["Carpet_Area_sqft"],
                "Floor_No": form.cleaned_data["Floor_No"],
                "Total_Floors": form.cleaned_data["Total_Floors"],
                "Property_Age_years": form.cleaned_data["Property_Age_years"],
                "Distance_to_Metro_km": form.cleaned_data["Distance_to_Metro_km"],
                "Distance_to_CityCenter_km": form.cleaned_data["Distance_to_CityCenter_km"],
                "Nearby_School_km": form.cleaned_data["Nearby_School_km"],
                "Nearby_Hospital_km": form.cleaned_data["Nearby_Hospital_km"],
                "Crime_Rate_Index": form.cleaned_data["Crime_Rate_Index"],
                "City": form.cleaned_data["City"],
                "Locality_Tier": form.cleaned_data["Locality_Tier"],
                "Furnishing": form.cleaned_data["Furnishing"],
                "Parking": parking_val,
                "Lift": lift_val,
                "Gated_Society": gated_val,
            }])

            if feature_cols:
                input_encoded = pd.get_dummies(input_data, dummy_na=True)
                input_encoded = input_encoded.reindex(columns=feature_cols, fill_value=0)
                predicted_price = float(model.predict(input_encoded)[0])
            else:
                predicted_price = float(model.predict(input_data)[0])

            final_price = max(0.0, predicted_price)

            result = {
                "price": final_price,
                "model_name": selected_model,
                "city": form.cleaned_data["City"],
                "area": form.cleaned_data["Super_Area_sqft"],
            }

            if request.user.is_authenticated:
                try:
                    Prediction.objects.create(
                        user=request.user,
                        city=form.cleaned_data["City"],
                        locality_tier=form.cleaned_data["Locality_Tier"],
                        bhk=int(form.cleaned_data["BHK"]),
                        bathrooms=int(form.cleaned_data["Bathrooms"]),
                        super_area_sqft=float(form.cleaned_data["Super_Area_sqft"]),
                        carpet_area_sqft=float(form.cleaned_data["Carpet_Area_sqft"]),
                        floor_no=int(form.cleaned_data["Floor_No"]),
                        total_floors=int(form.cleaned_data["Total_Floors"]),
                        property_age_years=int(form.cleaned_data["Property_Age_years"]),
                        parking=1 if form.cleaned_data["Parking"] == "Yes" else 0,
                        furnishing=form.cleaned_data["Furnishing"],
                        lift=True if form.cleaned_data["Lift"] == "Yes" else False,
                        gated_society=True if form.cleaned_data["Gated_Society"] == "Yes" else False,
                        distance_to_metro_km=float(form.cleaned_data["Distance_to_Metro_km"]),
                        distance_to_citycenter_km=float(form.cleaned_data["Distance_to_CityCenter_km"]),
                        nearby_school_km=float(form.cleaned_data["Nearby_School_km"]),
                        nearby_hospital_km=float(form.cleaned_data["Nearby_Hospital_km"]),
                        crime_rate_index=float(form.cleaned_data["Crime_Rate_Index"]),
                        predicted_price=round(final_price, 2),
                    )
                except Exception:
                    pass

        except (FileNotFoundError, KeyError, ValueError) as exc:
            error_message = str(exc)
        except Exception:
            error_message = (
                "Prediction failed. Check that the model "
                "and dataset features match, then retrain."
            )

    context = {
        "form": form,
        "result": result,
        "metrics_report": metrics_report,
        "error_message": error_message,
    }

    return render(
        request,
        "predictor/predict.html",
        context,
    )


@login_required
def history(request):
    predictions = Prediction.objects.filter(user=request.user).order_by("-created_at")
    return render(
        request,
        "predictor/history.html",
        {"predictions": predictions},
    )


@login_required
def prediction_detail(request, pk):
    if request.user.is_staff:
        prediction = get_object_or_404(Prediction, pk=pk)
    else:
        prediction = get_object_or_404(Prediction, pk=pk, user=request.user)

    return render(
        request,
        "predictor/prediction_detail.html",
        {"prediction": prediction},
    )


@login_required
def prediction_report_pdf(request, pk):
    if request.user.is_staff:
        prediction = get_object_or_404(Prediction, pk=pk)
    else:
        prediction = get_object_or_404(Prediction, pk=pk, user=request.user)

    pdf_bytes = generate_single_prediction_pdf(prediction)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="house_prediction_report_{prediction.pk}.pdf"'
    return response


@login_required
@require_POST
def delete_prediction(request, pk):
    if request.user.is_staff:
        prediction = get_object_or_404(Prediction, pk=pk)
    else:
        prediction = get_object_or_404(Prediction, pk=pk, user=request.user)

    prediction.delete()
    messages.success(request, "Prediction record deleted.")
    return redirect("history")