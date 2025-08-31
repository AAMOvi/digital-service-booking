# services/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone # Import timezone for default datetime

# Custom User Model to handle different roles (Admin/Customer)
# Inherits from Django's AbstractUser to get all standard user fields (username, email, password, etc.)
class CustomUser(AbstractUser):
    # Field to identify if the user is an administrator
    is_admin = models.BooleanField(default=False)
    # Field to identify if the user is a regular customer
    is_customer = models.BooleanField(default=True) # Default all new users to be customers

    # Add unique related_name arguments to avoid clashes with auth.User
    # This is necessary when extending AbstractUser and adding ManyToManyField or ForeignKey
    # relationships that might clash with the default User model's relationships.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_groups", # Custom related_name to avoid clash
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions", # Custom related_name to avoid clash
        related_query_name="custom_user",
    )

    def __str__(self):
        return self.username


# Service Model (FR-03: Admins can add/edit services)
class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # String representation of the service
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['name'] # Order services by name by default


# Booking Model (FR-05: Users can book a service, FR-09: Admins can change status)
class Booking(models.Model):
    # Link to the CustomUser who made the booking
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    # Link to the Service being booked
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    
    # New fields to store user information provided during booking
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()

    # Date and time for the booking
    booking_date_time = models.DateTimeField()
    # Date when the booking was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Status of the booking (e.g., Pending, Approved, Declined, Completed)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'), # Added Cancelled status for more flexibility
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        # String representation of the booking
        return f"{self.customer.username} - {self.service.name} on {self.booking_date_time.strftime('%Y-%m-%d %H:%M')}"
