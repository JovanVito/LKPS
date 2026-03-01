from django.contrib import admin
from django.urls import path, include # Pastikan 'include' diimpor

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ini adalah 'jembatan' yang benar ke rute aplikasi core kamu
    path('', include('core.urls')), 
]