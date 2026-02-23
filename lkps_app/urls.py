from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),      # Dashboard jadi halaman utama
    path('sampul/', views.halaman_sampul, name='sampul'), # Sampul pindah ke url /sampul/
    path('tabel-5-1/', views.tabel_5_1, name='tabel_5_1'),
    path('tabel-2a/', views.tabel_2a, name='tabel_2a'),
    path('tabel-3a/', views.tabel_3a, name='tabel_3a'),
    path('tim-penyusun/', views.tim_penyusun, name='tim_penyusun'),
    path('tabel-4/', views.tabel_4, name='tabel_4'),
    path('tabel-6/', views.tabel_6, name='tabel_6'),
    path('tabel-5-2/', views.tabel_5_2, name='tabel_5_2'),
    path('tabel-1/', views.tabel_1, name='tabel_1'),
    path('tabel-7/', views.tabel_7, name='tabel_7'),
    path('tabel-8/', views.tabel_8, name='tabel_8'),
    path('tabel-9/', views.tabel_9, name='tabel_9'),
]

