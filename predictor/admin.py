from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "city",
        "bhk",
        "super_area_sqft",
        "predicted_price",
        "created_at",
    )

    list_filter = ("city", "locality_tier", "bhk", "created_at")
    search_fields = ("user__username", "city")
    ordering = ("-created_at",)