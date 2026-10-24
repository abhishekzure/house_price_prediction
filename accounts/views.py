import csv
import json
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from predictor.models import Prediction
from predictor.reports import generate_user_report_pdf, generate_admin_report_pdf
from .forms import RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Registration successful. Welcome!'
            )
            return redirect('accounts:dashboard')
    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


class RoleBasedLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to

        if self.request.user.is_staff:
            return '/accounts/admin-dashboard/'

        return '/accounts/dashboard/'


@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('accounts:admin_dashboard')

    user_predictions = list(
        Prediction.objects.filter(user=request.user).order_by('-created_at')
    )
    total_predictions = len(user_predictions)

    if total_predictions > 0:
        prices = [float(p.predicted_price) for p in user_predictions]
        avg_price = sum(prices) / total_predictions
        max_price = max(prices)
        min_price = min(prices)
    else:
        avg_price = 0.0
        max_price = 0.0
        min_price = 0.0

    # Graph 1: Timeline of recent user predictions (up to 8 in chronological order)
    recent_trend = user_predictions[:8]
    recent_trend.reverse()
    trend_labels = [f"{p.city} ({p.bhk} BHK)" for p in recent_trend]
    trend_prices = [float(p.predicted_price) for p in recent_trend]

    # Graph 2: BHK Breakdown for user
    bhk_map = {}
    for p in user_predictions:
        key = f"{p.bhk} BHK"
        bhk_map[key] = bhk_map.get(key, 0) + 1
    bhk_labels = list(bhk_map.keys())
    bhk_counts = list(bhk_map.values())

    # Graph 3: City breakdown for user
    city_map = {}
    for p in user_predictions:
        city_map[p.city] = city_map.get(p.city, 0) + 1
    user_city_labels = list(city_map.keys())
    user_city_counts = list(city_map.values())

    context = {
        'total_predictions': total_predictions,
        'avg_price': avg_price,
        'max_price': max_price,
        'min_price': min_price,
        'recent_predictions': user_predictions[:5],
        'trend_labels_json': json.dumps(trend_labels),
        'trend_prices_json': json.dumps(trend_prices),
        'bhk_labels_json': json.dumps(bhk_labels),
        'bhk_counts_json': json.dumps(bhk_counts),
        'user_city_labels_json': json.dumps(user_city_labels),
        'user_city_counts_json': json.dumps(user_city_counts),
    }
    return render(
        request,
        'accounts/dashboard.html',
        context,
    )


@staff_member_required
def admin_dashboard(request):
    users = (
        User.objects
        .annotate(prediction_count=Count('house_predictions'))
        .order_by('-date_joined')
    )
    predictions = (
        Prediction.objects
        .select_related('user')
        .order_by('-created_at')[:100]
    )

    total_users = User.objects.count()
    total_predictions = Prediction.objects.count()
    avg_price_result = Prediction.objects.aggregate(avg=Avg('predicted_price'))
    avg_price = avg_price_result['avg'] or 0.0

    metrics_report = None
    metrics_path = Path(settings.BASE_DIR) / "model" / "model_metrics.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, "r", encoding="utf-8") as file:
                metrics_report = json.load(file)
        except Exception:
            metrics_report = None

    # Graph 1: Average Price by City
    city_qs = (
        Prediction.objects
        .values('city')
        .annotate(avg_price=Avg('predicted_price'), count=Count('id'))
        .order_by('city')
    )
    if city_qs.exists():
        admin_city_labels = [c['city'] for c in city_qs]
        admin_city_prices = [round(float(c['avg_price']), 2) for c in city_qs]
        admin_city_counts = [c['count'] for c in city_qs]
    else:
        # Benchmark averages from training dataset
        admin_city_labels = ['Bangalore', 'Hyderabad', 'Mumbai', 'Nagpur', 'Pune']
        admin_city_prices = [9801246.0, 7653229.0, 16182480.0, 5508934.0, 8808134.0]
        admin_city_counts = [0, 0, 0, 0, 0]

    # Graph 2: Locality Tier Distribution
    tier_qs = (
        Prediction.objects
        .values('locality_tier')
        .annotate(count=Count('id'))
        .order_by('locality_tier')
    )
    if tier_qs.exists():
        admin_tier_labels = [t['locality_tier'] for t in tier_qs]
        admin_tier_counts = [t['count'] for t in tier_qs]
    else:
        admin_tier_labels = ['Budget', 'Mid', 'Premium']
        admin_tier_counts = [0, 0, 0]

    # Graph 3: Timeline of Recent Predictions
    recent_admin_preds = list(Prediction.objects.order_by('-created_at')[:10])
    recent_admin_preds.reverse()
    admin_trend_labels = [f"#{p.id} {p.city}" for p in recent_admin_preds]
    admin_trend_prices = [float(p.predicted_price) for p in recent_admin_preds]

    context = {
        'users': users,
        'predictions': predictions,
        'total_users': total_users,
        'total_predictions': total_predictions,
        'avg_price': avg_price,
        'metrics_report': metrics_report,
        'admin_city_labels_json': json.dumps(admin_city_labels),
        'admin_city_prices_json': json.dumps(admin_city_prices),
        'admin_city_counts_json': json.dumps(admin_city_counts),
        'admin_tier_labels_json': json.dumps(admin_tier_labels),
        'admin_tier_counts_json': json.dumps(admin_tier_counts),
        'admin_trend_labels_json': json.dumps(admin_trend_labels),
        'admin_trend_prices_json': json.dumps(admin_trend_prices),
    }
    return render(
        request,
        'accounts/admin_dashboard.html',
        context,
    )


def export_predictions_csv(predictions, filename):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'User',
        'City',
        'Locality_Tier',
        'BHK',
        'Bathrooms',
        'Super_Area_sqft',
        'Carpet_Area_sqft',
        'Floor_No',
        'Total_Floors',
        'Property_Age_years',
        'Furnishing',
        'Parking',
        'Lift',
        'Gated_Society',
        'Distance_to_Metro_km',
        'Distance_to_CityCenter_km',
        'Nearby_School_km',
        'Nearby_Hospital_km',
        'Crime_Rate_Index',
        'Predicted_Price_INR',
        'Created_At',
    ])

    for p in predictions:
        writer.writerow([
            p.id,
            p.user.username,
            p.city,
            p.locality_tier,
            p.bhk,
            p.bathrooms,
            p.super_area_sqft,
            p.carpet_area_sqft,
            p.floor_no,
            p.total_floors,
            p.property_age_years,
            p.furnishing,
            'Yes' if p.parking else 'No',
            'Yes' if p.lift else 'No',
            'Yes' if p.gated_society else 'No',
            p.distance_to_metro_km,
            p.distance_to_citycenter_km,
            p.nearby_school_km,
            p.nearby_hospital_km,
            p.crime_rate_index,
            float(p.predicted_price),
            p.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])

    return response


@login_required
def user_predictions_report_pdf(request):
    predictions = list(Prediction.objects.filter(user=request.user).order_by('-created_at'))
    pdf_bytes = generate_user_report_pdf(request.user, predictions)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="my_predictions_report_{request.user.username}.pdf"'
    return response


@login_required
def user_predictions_report_csv(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    return export_predictions_csv(predictions, f"my_predictions_{request.user.username}.csv")


@staff_member_required
def admin_predictions_report_pdf(request):
    predictions = list(Prediction.objects.select_related('user').order_by('-created_at'))
    total_users = User.objects.count()
    total_predictions = len(predictions)
    avg_price = (
        sum(float(p.predicted_price) for p in predictions) / total_predictions
        if total_predictions > 0 else 0.0
    )

    metrics_report = None
    metrics_path = Path(settings.BASE_DIR) / "model" / "model_metrics.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, "r", encoding="utf-8") as file:
                metrics_report = json.load(file)
        except Exception:
            metrics_report = None

    pdf_bytes = generate_admin_report_pdf(
        predictions, total_users, total_predictions, avg_price, metrics_report
    )
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="admin_system_predictions_report.pdf"'
    return response


@staff_member_required
def admin_predictions_report_csv(request):
    predictions = Prediction.objects.select_related('user').order_by('-created_at')
    return export_predictions_csv(predictions, "system_all_predictions.csv")


@staff_member_required
@require_POST
def admin_toggle_user_active(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
    else:
        target_user.is_active = not target_user.is_active
        target_user.save()
        status_str = "activated" if target_user.is_active else "deactivated"
        messages.success(request, f"User '{target_user.username}' has been {status_str}.")
    return redirect('accounts:admin_dashboard')


@staff_member_required
@require_POST
def admin_toggle_user_staff(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot modify your own staff permissions.")
    else:
        target_user.is_staff = not target_user.is_staff
        target_user.save()
        status_str = "granted staff role" if target_user.is_staff else "revoked staff role"
        messages.success(request, f"User '{target_user.username}' has been {status_str}.")
    return redirect('accounts:admin_dashboard')


@staff_member_required
@require_POST
def admin_delete_prediction(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk)
    prediction.delete()
    messages.success(request, f"Prediction record #{pk} was successfully deleted.")
    return redirect('accounts:admin_dashboard')


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
