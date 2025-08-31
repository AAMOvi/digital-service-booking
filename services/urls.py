# services/urls.py

from django.urls import path
from . import views # Import views from the current app
from django.contrib.auth import views as auth_views # Import Django's built-in auth views

urlpatterns = [
    # Home Page (Landing Page)
    path('', views.home, name='home'),

    # User Authentication (FR-01)
    path('register/', views.register, name='register'), # User registration
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # User login
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), # User logout

    # Service Listing (FR-04)
    path('services/', views.service_list, name='service_list'),

    # Booking a Service (FR-05)
    path('book/<int:service_id>/', views.book_service, name='book_service'),

    # User Dashboard (FR-07, FR-08)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Booking History (FR-07)
    path('history/', views.booking_history, name='booking_history'),

    # Admin-specific views (Optional, for now we rely on Django Admin for FR-03, FR-09)
    # If you later want a custom admin dashboard outside of Django's default, you'd add paths here.

    # Payment Simulator (FR-05, now with booking_id)
    path('pay/<int:booking_id>/', views.payment_simulator, name='payment_simulator'),

    # API Endpoint for Payment Confirmation
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
]
