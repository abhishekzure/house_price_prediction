from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from predictor.models import Prediction


class PredictorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="predict_user",
            password="testpassword123",
            email="pred@example.com",
        )

    def test_predict_requires_login(self):
        response = self.client.get(reverse("predict_price"))
        self.assertEqual(response.status_code, 302)

    def test_predict_page_authenticated(self):
        self.client.login(username="predict_user", password="testpassword123")
        response = self.client.get(reverse("predict_price"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "predictor/predict.html")

    def test_predict_post_and_history(self):
        self.client.login(username="predict_user", password="testpassword123")
        post_data = {
            "BHK": 2,
            "Bathrooms": 2,
            "Super_Area_sqft": 1000.0,
            "Floor_No": 3,
            "Property_Age_years": 2,
            "Parking": "Yes",
            "Lift": "Yes",
            "City": "Mumbai",
        }
        response = self.client.post(reverse("predict_price"), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Estimated House Price")

        # Verify saved in Prediction model
        self.assertEqual(Prediction.objects.filter(user=self.user).count(), 1)
        saved = Prediction.objects.filter(user=self.user).first()
        self.assertEqual(saved.city, "Mumbai")
        self.assertEqual(saved.bhk, 2)

        # Verify history page
        history_response = self.client.get(reverse("history"))
        self.assertEqual(history_response.status_code, 200)
        self.assertContains(history_response, "Mumbai")

        # Verify prediction detail page
        detail_response = self.client.get(reverse("predictor:prediction_detail", args=[saved.pk]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Mumbai")

        # Verify delete prediction
        del_response = self.client.post(reverse("predictor:delete_prediction", args=[saved.pk]), follow=True)
        self.assertEqual(del_response.status_code, 200)
        self.assertEqual(Prediction.objects.filter(user=self.user).count(), 0)

    def test_predict_all_18_features(self):
        self.client.login(username="predict_user", password="testpassword123")
        post_data = {
            "City": "Pune",
            "Locality_Tier": "Premium",
            "BHK": 3,
            "Bathrooms": 3,
            "Super_Area_sqft": 1500.0,
            "Carpet_Area_sqft": 1200.0,
            "Floor_No": 5,
            "Total_Floors": 12,
            "Property_Age_years": 4,
            "Furnishing": "Fully-Furnished",
            "Parking": "Yes",
            "Lift": "Yes",
            "Gated_Society": "Yes",
            "Distance_to_Metro_km": 1.2,
            "Distance_to_CityCenter_km": 8.5,
            "Nearby_School_km": 0.8,
            "Nearby_Hospital_km": 1.5,
            "Crime_Rate_Index": 15.0,
        }
        response = self.client.post(reverse("predict_price"), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Estimated House Price")

        saved = Prediction.objects.filter(user=self.user).latest("created_at")
        self.assertEqual(saved.city, "Pune")
        self.assertEqual(saved.locality_tier, "Premium")
        self.assertEqual(saved.bhk, 3)
        self.assertEqual(saved.bathrooms, 3)
        self.assertEqual(saved.super_area_sqft, 1500.0)
        self.assertEqual(saved.carpet_area_sqft, 1200.0)
        self.assertEqual(saved.floor_no, 5)
        self.assertEqual(saved.total_floors, 12)
        self.assertEqual(saved.property_age_years, 4)
        self.assertEqual(saved.furnishing, "Fully-Furnished")
        self.assertEqual(saved.parking, 1)
        self.assertTrue(saved.lift)
        self.assertTrue(saved.gated_society)
        self.assertEqual(saved.distance_to_metro_km, 1.2)
        self.assertEqual(saved.distance_to_citycenter_km, 8.5)
        self.assertEqual(saved.nearby_school_km, 0.8)
        self.assertEqual(saved.nearby_hospital_km, 1.5)
        self.assertEqual(saved.crime_rate_index, 15.0)

        # Check detail page displays all fields
        detail_response = self.client.get(reverse("predictor:prediction_detail", args=[saved.pk]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Pune")
        self.assertContains(detail_response, "Premium")
        self.assertContains(detail_response, "Fully-Furnished")
        self.assertContains(detail_response, "1.2 km")
        self.assertContains(detail_response, "15.0")

    def test_single_prediction_pdf_report(self):
        self.client.login(username="predict_user", password="testpassword123")
        prediction = Prediction.objects.create(
            user=self.user,
            city="Pune",
            locality_tier="Mid",
            bhk=2,
            bathrooms=2,
            super_area_sqft=1000.0,
            carpet_area_sqft=800.0,
            floor_no=2,
            total_floors=5,
            property_age_years=3,
            parking=1,
            furnishing="Semi-Furnished",
            lift=True,
            gated_society=True,
            distance_to_metro_km=1.5,
            distance_to_citycenter_km=5.0,
            nearby_school_km=1.0,
            nearby_hospital_km=1.2,
            crime_rate_index=20.0,
            predicted_price=5500000.0,
        )
        url = reverse("predictor:prediction_report_pdf", args=[prediction.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(len(response.content) > 100)

