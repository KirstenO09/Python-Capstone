from django.urls import path
from appo import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('new/', views.create_appointment, name='create_appointment'),
    path('edit/<int:pk>/', views.update_appointment, name='update_appointment'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
]