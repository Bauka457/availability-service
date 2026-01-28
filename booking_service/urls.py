from django.contrib import admin
from django.urls import path, include
from bookings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('bookings/', views.bookings_list_page, name='bookings_list_page'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),  # Новая админ-панель
    path('api/bookings/', include('bookings.urls')),
]