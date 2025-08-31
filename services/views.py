# services/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout # Import login/logout functions
from django.contrib.auth.decorators import login_required, user_passes_test # For access control
from django.contrib import messages # For displaying messages to the user
from django.db.models import Q # For complex queries in history/dashboard
from django.http import JsonResponse # Import this for the new API view
import json # Don't forget this import
from datetime import timedelta # For time calculations

from .forms import CustomUserCreationForm, BookingForm # Import your custom forms
from .models import Service, Booking, CustomUser # Import your models
from django.utils import timezone # For current time in booking validation

# --- Helper Functions for Access Control ---
# These functions check user roles for decorators

def is_admin(user):
    # Check if the user is an admin
    return user.is_authenticated and user.is_admin

def is_customer(user):
    # Check if the user is a customer
    return user.is_authenticated and user.is_customer

# --- Public Views ---

# Home Page (Landing Page - NFR-02: intuitive, user-friendly, mobile responsive)
def home(request):
    # Fetches a few services to display on the landing page
    # You can customize how many services to show or filter them.
    featured_services = Service.objects.all()[:4] # Get first 4 services
    return render(request, 'home.html', {'featured_services': featured_services})

# User Registration (FR-01)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True # Ensure the new user is a customer
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login') # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# Service Listing (FR-04)
def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

# Booking a Service (FR-05)
@login_required
@user_passes_test(is_customer, login_url='login')
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service
            # Validate booking date and time to be in the future
            if booking.booking_date_time < timezone.now():
                messages.error(request, "The booking date and time must be in the future.")
            else:
                booking.save()
                messages.success(request, "Your booking request has been submitted successfully!")
                return redirect('payment_simulator', booking_id=booking.id) # Redirect to the payment simulator
    else:
        # Pass the initial service to the form
        form = BookingForm()
    
    return render(request, 'book_service.html', {'form': form, 'service': service})

# User Dashboard (FR-07, FR-08)
@login_required
@user_passes_test(is_customer, login_url='login')
def dashboard(request):
    now = timezone.now()
    # Filter bookings that are upcoming (in the future)
    upcoming_bookings = Booking.objects.filter(
        customer=request.user,
        status__in=['Pending', 'Approved']
    ).filter(
        booking_date_time__gt=now # Bookings after now
    ).order_by('booking_date_time')
    
    # Filter bookings that are in the past
    past_bookings = Booking.objects.filter(
        Q(customer=request.user) & 
        (Q(status='Completed') | Q(status='Declined') | Q(status='Cancelled'))
    ).filter(
        booking_date_time__lte=now # Bookings before now
    ).order_by('-booking_date_time')

    return render(request, 'dashboard.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    })

# Booking History (FR-07)
@login_required
@user_passes_test(is_customer, login_url='login')
def booking_history(request):
    # Get all bookings for the current customer, ordered by most recent first
    all_bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date_time')
    return render(request, 'booking_history.html', {'bookings': all_bookings})

# --- Admin Views (FR-08, FR-09) ---
# For now, most admin management will be handled via the Django Admin Panel.
@login_required
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    total_services = Service.objects.count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='Pending').count()
    # You can add more statistics here
    return render(request, 'admin_dashboard.html', {
        'total_services': total_services,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings
    })
    
# New View: Payment Simulator (FR-05)
@login_required
@user_passes_test(is_customer, login_url='login')
def payment_simulator(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    return render(request, 'payment_simulator.html', {'booking': booking})

# New API Endpoint: Confirm Payment
@login_required
def confirm_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            booking_id = data.get('booking_id')
            booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
            
            # Update the booking status to 'Completed' or 'Confirmed'
            booking.status = 'Completed'
            booking.save()
            
            messages.success(request, f"Booking #{booking.id} has been successfully paid for and confirmed.")
            return JsonResponse({'status': 'success', 'message': 'Payment confirmed successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
