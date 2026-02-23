from django.contrib import admin
from django.urls import path, include # Pastikan 'include' sudah di-import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Ini adalah 'jembatan' ke aplikasi core kamu
]