from django.contrib import admin
from .models import Hairstyle, Appointment, Inquiry


@admin.register(Hairstyle)
class HairstyleAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_minutes', 'is_available']
    list_filter = ['is_available']
    search_fields = ['name', 'description']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_email', 'hairstyle', 'appointment_date', 'appointment_time', 'created_at']
    list_filter = ['appointment_date', 'hairstyle']
    search_fields = ['customer_name', 'customer_email']
    date_hierarchy = 'appointment_date'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'submitted_at']
    list_filter = ['status', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['submitted_at']

    # Allow changing status
    list_editable = ['status']

    # Show newest first
    ordering = ['-submitted_at']