from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # Ini untuk halaman muka
    path('export-word/', views.export_to_word, name='export_word'),
]