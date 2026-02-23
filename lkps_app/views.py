# lkps_app/views.py
from django.shortcuts import render

def halaman_sampul(request):
    # Di sini nanti kita bisa menambahkan logika untuk mengambil data dari database
    # Untuk sekarang, kita fokus merender (menampilkan) UI-nya dulu.
    return render(request, 'lkps_app/sampul.html')

def dashboard(request):
    return render(request, 'lkps_app/dashboard.html')

def tabel_5_1(request):
    return render(request, 'lkps_app/tabel_5_1.html')

def tabel_2a(request):
    return render(request, 'lkps_app/tabel_2a.html')

def tabel_3a(request):
    return render(request, 'lkps_app/tabel_3a.html')

def tim_penyusun(request):
    return render(request, 'lkps_app/tim_penyusun.html')

def tabel_4(request):
    return render(request, 'lkps_app/tabel_4.html')

def tabel_6(request):
    return render(request, 'lkps_app/tabel_6.html')

def tabel_5_2(request):
    return render(request, 'lkps_app/tabel_5_2.html')

def tabel_1(request):
    return render(request, 'lkps_app/tabel_1.html')

def tabel_7(request):
    return render(request, 'lkps_app/tabel_7.html')

def tabel_8(request):
    return render(request, 'lkps_app/tabel_8.html')

def tabel_9(request):
    return render(request, 'lkps_app/tabel_9.html')