from django.contrib import admin
from django.urls import path, include
from predictor import views as predictor_views


urlpatterns = [
    path('', predictor_views.index, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('predictor/', include('predictor.urls')),
    path('predict/', predictor_views.predict_price, name='predict_price'),
    path('history/', predictor_views.history, name='history'),
    path('history/<int:pk>/', predictor_views.prediction_detail, name='prediction_detail'),
    path('history/<int:pk>/report/pdf/', predictor_views.prediction_report_pdf, name='prediction_report_pdf'),
    path('history/<int:pk>/delete/', predictor_views.delete_prediction, name='delete_prediction'),
]
