from django.urls import path
from . import views

app_name = "predictor"

urlpatterns = [
    path("predict/", views.predict_price, name="predict_price"),
    path("predict-run/", views.predict_price, name="predict"),
    path("history/", views.history, name="history"),
    path("history/<int:pk>/", views.prediction_detail, name="prediction_detail"),
    path("history/<int:pk>/report/pdf/", views.prediction_report_pdf, name="prediction_report_pdf"),
    path("history/<int:pk>/delete/", views.delete_prediction, name="delete_prediction"),
]
