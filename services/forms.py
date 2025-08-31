# services/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Service, Booking
from django.forms import DateTimeInput

# Get the CustomUser model dynamically
CustomUser = get_user_model()

# Form for User Registration (FR-01)
class CustomUserCreationForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm to include the 'email' field.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

# Form for Booking a Service (FR-05)
class BookingForm(forms.ModelForm):
    """
    Form for a customer to book a service.
    Includes fields for the booking date/time, and user details like name, contact, and address.
    """
    name = forms.CharField(max_length=100, label="Full Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_number = forms.CharField(max_length=15, label="Contact Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, label="Address", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = Booking
        fields = ['booking_date_time', 'name', 'contact_number', 'address']
        widgets = {
            'booking_date_time': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a class to the booking_date_time field for styling
        self.fields['booking_date_time'].widget.attrs['class'] = 'form-control'
