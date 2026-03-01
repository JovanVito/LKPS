from django.urls import path
from . import views

urlpatterns = [
    # --- DASHBOARD ---
    # Mengarah ke views.dashboard (views.home sudah kita hapus agar tidak duplikat)
    path('', views.dashboard, name='dashboard'),
    
    # --- IDENTITAS & TIM PENYUSUN ---
    # Rute 'sampul/' dihapus karena 'identitas/' sudah memanggil form yang benar
    path('identitas/', views.identitas_pengusul, name='identitas'),
    path('tim_penyusun/', views.tim_penyusun, name='tim_penyusun'),
    path('import_excel_lkps/', views.import_excel_lkps, name='import_excel'),
    # --- KRITERIA 1 - 3 ---
    # Mengarah ke fungsi views masing-masing, BUKAN ke views.home lagi
    path('tabel_1/', views.tabel_1, name='tabel_1'),
    path('tabel_2a/', views.tabel_2a, name='tabel_2a'),
    path('tabel_3a/', views.tabel_3a, name='tabel_3a'),
    
    # --- KRITERIA 4 - 6 ---
    path('tabel_4/', views.tabel_4, name='tabel_4'),
    path('tabel_5_1/', views.tabel_5_1, name='tabel_5_1'),
    path('tabel_5_2/', views.tabel_5_2, name='tabel_5_2'),
    path('tabel_6/', views.tabel_6, name='tabel_6'),
    
    # --- KRITERIA 7 - 9 ---
    path('tabel_7/', views.tabel_7, name='tabel_7'),
    path('tabel_8/', views.tabel_8, name='tabel_8'),
    path('tabel_9/', views.tabel_9, name='tabel_9'),
    
    # (Placeholder untuk tabel_10 jika view-nya belum ada, sementara arahkan ke dashboard)
    path('tabel_10/', views.dashboard, name='tabel_10'),
    
    # --- FITUR UTAMA ---
    path('input_penelitian/', views.input_penelitian, name='input_penelitian'),
]