from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from predictor.models import Prediction


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="regular_user",
            password="testpassword123",
            email="reg@example.com",
            first_name="Regular",
            last_name="User",
        )
        self.staff_user = User.objects.create_user(
            username="staff_user",
            password="testpassword123",
            email="staff@example.com",
            is_staff=True,
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_register_page_renders(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_dashboard_redirects_unauthenticated(self):
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_user_dashboard_authenticated(self):
        self.client.login(username="regular_user", password="testpassword123")
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/dashboard.html")

    def test_admin_dashboard_for_staff(self):
        self.client.login(username="staff_user", password="testpassword123")
        response = self.client.get(reverse("accounts:admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/admin_dashboard.html")
        self.assertContains(response, "Admin Dashboard")
        self.assertContains(response, "User Management")
        self.assertContains(response, "regular_user")

    def test_admin_dashboard_blocks_regular_user(self):
        self.client.login(username="regular_user", password="testpassword123")
        response = self.client.get(reverse("accounts:admin_dashboard"))
        # staff_member_required redirects non-staff users
        self.assertEqual(response.status_code, 302)

    def test_admin_toggle_user_active(self):
        self.client.login(username="staff_user", password="testpassword123")
        self.assertTrue(self.user.is_active)

        url = reverse("accounts:admin_toggle_user_active", args=[self.user.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        # Toggle back
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_admin_toggle_user_staff(self):
        self.client.login(username="staff_user", password="testpassword123")
        self.assertFalse(self.user.is_staff)

        url = reverse("accounts:admin_toggle_user_staff", args=[self.user.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)

    def test_admin_cannot_deactivate_self(self):
        self.client.login(username="staff_user", password="testpassword123")
        url = reverse("accounts:admin_toggle_user_active", args=[self.staff_user.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.staff_user.refresh_from_db()
        self.assertTrue(self.staff_user.is_active)

    def test_admin_delete_prediction(self):
        self.client.login(username="staff_user", password="testpassword123")
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
        self.assertEqual(Prediction.objects.count(), 1)

        url = reverse("accounts:admin_delete_prediction", args=[prediction.pk])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Prediction.objects.count(), 0)

    def test_profile_page_authenticated(self):
        self.client.login(username="regular_user", password="testpassword123")
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertContains(response, "regular_user")

    def test_user_dashboard_graphs_and_stats(self):
        self.client.login(username="regular_user", password="testpassword123")
        Prediction.objects.create(
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
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "userTrendChart")
        self.assertContains(response, "userBhkChart")
        self.assertContains(response, "Download PDF Report")

    def test_user_reports_pdf_and_csv(self):
        self.client.login(username="regular_user", password="testpassword123")
        Prediction.objects.create(
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
        # PDF report
        pdf_res = self.client.get(reverse("accounts:user_predictions_report_pdf"))
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res["Content-Type"], "application/pdf")
        self.assertTrue(len(pdf_res.content) > 100)

        # CSV report
        csv_res = self.client.get(reverse("accounts:user_predictions_report_csv"))
        self.assertEqual(csv_res.status_code, 200)
        self.assertIn("text/csv", csv_res["Content-Type"])
        self.assertContains(csv_res, "Pune")

    def test_admin_reports_pdf_and_csv(self):
        self.client.login(username="staff_user", password="testpassword123")
        Prediction.objects.create(
            user=self.user,
            city="Mumbai",
            locality_tier="Premium",
            bhk=3,
            bathrooms=3,
            super_area_sqft=1400.0,
            carpet_area_sqft=1100.0,
            floor_no=5,
            total_floors=15,
            property_age_years=2,
            parking=1,
            furnishing="Fully-Furnished",
            lift=True,
            gated_society=True,
            distance_to_metro_km=0.5,
            distance_to_citycenter_km=3.0,
            nearby_school_km=0.5,
            nearby_hospital_km=0.8,
            crime_rate_index=15.0,
            predicted_price=12500000.0,
        )

        # Admin PDF report
        pdf_res = self.client.get(reverse("accounts:admin_predictions_report_pdf"))
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res["Content-Type"], "application/pdf")
        self.assertTrue(len(pdf_res.content) > 100)

        # Admin CSV report
        csv_res = self.client.get(reverse("accounts:admin_predictions_report_csv"))
        self.assertEqual(csv_res.status_code, 200)
        self.assertIn("text/csv", csv_res["Content-Type"])
        self.assertContains(csv_res, "Mumbai")

