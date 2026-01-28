from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('create/', views.create_booking, name='create_booking'),
    path('list/', views.list_bookings, name='list_bookings'),
    path('<int:booking_id>/', views.get_booking_detail, name='get_booking_detail'),
    path('<int:booking_id>/update/', views.update_booking, name='update_booking'),
    path('<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('health/', views.health_check, name='health_check'),
    path('check-service-b/', views.check_service_b_status, name='check_service_b'),
]