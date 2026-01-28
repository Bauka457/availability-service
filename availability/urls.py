from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.check_availability, name='check_availability'),
    path('health/', views.health_check, name='health_check'),
    path('checks/', views.get_all_checks, name='get_all_checks'),
    path('bookings-list/', views.get_all_bookings, name='get_all_bookings'),
]