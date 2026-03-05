# appointments/urls.py
from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # Home page with hairstyle cards
    path("", views.home, name="home"),

    # Hairstyles Detail Page
    path("hairstyles/<int:pk>/", views.hairstyle_detail, name="hairstyle_detail"),

    # Booking form
    path("book/", views.create_appointment, name="create_appointment"),

    # Confirmation after booking
    path("confirmation/<int:pk>/", views.appointment_confirmation, name="appointment_confirmation"),

    # Admin view - all appointments
    path("appointments/", views.appointment_list, name="appointment_list"),

    # Edit appointment
    path("appointments/edit/<int:pk>/", views.update_appointment, name="update_appointment"),

    # Cancel appointment
    path("appointments/cancel/<int:pk>/", views.delete_appointment, name="delete_appointment"),

    # Contact URLs
    path("contact/", views.contact, name="contact"),
    path("contact/confirmation/<int:pk>/", views.contact_confirmation, name="contact_confirmation"),

    # Inspiration Gallery
    path("inspiration/", views.inspiration_gallery, name="inspiration_gallery"),

    # Natural Hair Tips
    path("natural-hair-tips/", views.natural_hair_tips, name="natural_hair_tips"),
]
