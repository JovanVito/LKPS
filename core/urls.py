from django.urls import path
from . import views

urlpatterns = [
    # --- AUTHENTICATION & DASHBOARD ---
    # Mengalihkan root ke halaman login sesuai alur frontend
    path('', views.login_view, name='login'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # --- IDENTITAS & MASTER DATA ---
    path('identitas/', views.identitas_pengusul, name='identitas'),
    path('program-studi/', views.program_studi, name='program_studi'), # Penambahan baru
    path('tim_penyusun/', views.tim_penyusun, name='tim_penyusun'),
    path('import_excel_lkps/', views.import_excel_lkps, name='import_excel'),

    # --- KRITERIA 1 - 3 ---
    path('tabel_1/', views.tabel_1, name='tabel_1'),
    path('tabel_2a/', views.tabel_2a, name='tabel_2a'),
    path('tabel_3a/', views.tabel_3a, name='tabel_3a'),
    
    # --- KRITERIA 4 - 6 ---
    path('tabel_4/', views.tabel_4, name='tabel_4'),
    path('tabel_5_1/', views.tabel_5_1, name='tabel_5_1'),
    path('tabel-5-2/', views.tabel_5_2, name='tabel_5_2'),
    path('tabel_6/', views.tabel_6, name='tabel_6'),
    
    # --- KRITERIA 7 - 9 ---
    path('tabel_7/', views.tabel_7, name='tabel_7'),
    path('tabel_8/', views.tabel_8, name='tabel_8'),
    path('tabel_9/', views.tabel_9, name='tabel_9'),
    path('tabel_kepuasan/', views.tabel_kepuasan, name='tabel_kepuasan'), # Penambahan baru
    
    # --- LAINNYA & FITUR UTAMA ---
    path('tabel_10/', views.dashboard, name='tabel_10'),
    path('input_penelitian/', views.input_penelitian, name='input_penelitian'),
]