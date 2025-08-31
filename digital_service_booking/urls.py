# digital_service_booking/urls.py

from django.contrib import admin
from django.urls import path, include # Import include
from django.views.generic import TemplateView # For simple static pages like home

urlpatterns = [
    path('admin/', admin.site.urls), # Django admin panel
    path('', include('services.urls')), # Include URLs from your 'services' app
]

