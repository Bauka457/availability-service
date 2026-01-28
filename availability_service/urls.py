from django.contrib import admin
from django.urls import path, include
from availability import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),  # Главная страница
    path('api/', include('availability.urls')),
]