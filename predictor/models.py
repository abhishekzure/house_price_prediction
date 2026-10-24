
from django.conf import settings
from django.db import models


class Prediction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="house_predictions",
    )

    city = models.CharField(max_length=100)
    locality_tier = models.CharField(max_length=30)
    bhk = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()

    super_area_sqft = models.FloatField()
    carpet_area_sqft = models.FloatField()

    floor_no = models.PositiveSmallIntegerField()
    total_floors = models.PositiveSmallIntegerField()
    property_age_years = models.PositiveSmallIntegerField()

    parking = models.PositiveSmallIntegerField()
    furnishing = models.CharField(max_length=40)
    lift = models.BooleanField()
    gated_society = models.BooleanField()

    distance_to_metro_km = models.FloatField()
    distance_to_citycenter_km = models.FloatField()
    nearby_school_km = models.FloatField()
    nearby_hospital_km = models.FloatField()
    crime_rate_index = models.FloatField()

    predicted_price = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - ₹{self.predicted_price}"
