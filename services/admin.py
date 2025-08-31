# services/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Service, Booking

# Register your CustomUser model with the admin site.
# We extend Django's default UserAdmin to ensure all default user fields are handled.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the fieldsets for display in the admin panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin', 'is_customer')}),
    )
    # Add your custom fields to the list_display for viewing in the admin list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'is_customer')
    # Add filters for easier searching in the admin list
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_admin', 'is_customer')


# Register the Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description') # Fields to display in the list view
    search_fields = ('name', 'description') # Fields to enable search by
    list_filter = ('price',) # Fields to enable filtering by


# Register the Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # This list_display defines the columns shown in the admin list view.
    # It includes the custom fields like 'customer', 'service', and 'status'.
    list_display = ('customer', 'service', 'booking_date_time', 'status', 'created_at')
    
    # These list_filter fields create a filter sidebar on the right.
    # This is perfect for filtering bookings by 'status'.
    list_filter = ('status', 'booking_date_time', 'service')
    
    # This enables a search box for quick searching.
    search_fields = ('customer__username', 'service__name') 
    
    # raw_id_fields is good for performance with large datasets.
    raw_id_fields = ('customer', 'service') 
    
    # This is the key part! It adds your custom actions to the admin panel's dropdown.
    actions = ['mark_as_approved', 'mark_as_declined', 'mark_as_completed'] 

    # Custom admin action to mark selected bookings as Approved.
    def mark_as_approved(self, request, queryset):
        queryset.update(status='Approved')
        self.message_user(request, "Selected bookings marked as Approved.")
    mark_as_approved.short_description = "Mark selected bookings as Approved"

    # Custom admin action to mark selected bookings as Declined.
    def mark_as_declined(self, request, queryset):
        queryset.update(status='Declined')
        self.message_user(request, "Selected bookings marked as Declined.")
    mark_as_declined.short_description = "Mark selected bookings as Declined"

    # Custom admin action to mark selected bookings as Completed.
    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completed')
        self.message_user(request, "Selected bookings marked as Completed.")
    mark_as_completed.short_description = "Mark selected bookings as Completed"
