import os
import io
import pandas as pd
from docxtpl import DocxTemplate
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from .models import (
    IdentitasPengusul, PenelitianDTPR, Tabel1Kerjasama, 
    DataMahasiswa, SumberPendanaan, TenagaKependidikan, 
    PublikasiMahasiswa, DosenTetap, PenggunaanDana, Kurikulum, SistemTataKelola
)

# --- HELPER: PEMBERSIH ANGKA ---
def to_clean_float(val):
    """Konversi format angka Indonesia/Excel ke float standar"""
    if pd.isna(val): return 0.0
    try:
        s = str(val).replace('Rp', '').replace(' ', '')
        if ',' in s and '.' in s: s = s.replace('.', '').replace(',', '.')
        elif ',' in s: s = s.replace(',', '.')
        return float(s)
    except: return 0.0

# --- 1. FITUR MASTER IMPORT EXCEL (TABEL 2, 3, 4) ---

def import_excel_lkps(request):
    """Master Import: Mendukung mapping kolom untuk Tabel 2, 3, dan 4"""
    if request.method == 'POST' and request.FILES.get('file_excel'):
        file = request.FILES['file_excel']
        try:
            xls = pd.ExcelFile(file)
            sheet_names = xls.sheet_names
            logs = []

            with transaction.atomic():
                # --- PROSES TABEL 2A (MAHASISWA) ---
                s2a = next((s for s in sheet_names if '2' in s.lower()), None)
                if s2a:
                    df2 = pd.read_excel(xls, s2a)
                    df2.columns = [str(c).strip() for c in df2.columns]
                    DataMahasiswa.objects.all().delete()
                    for _, row in df2.iterrows():
                        DataMahasiswa.objects.create(
                            tahun_akademik=str(row.get('Tahun Akademik', 'TS')),
                            daya_tampung=int(to_clean_float(row.get('Daya Tampung'))),
                            pendaftar=int(to_clean_float(row.get('Pendaftar'))),
                            lulus_seleksi=int(to_clean_float(row.get('Lulus Seleksi'))),
                            mhs_baru_reguler=int(to_clean_float(row.get('Maba Reguler'))),
                            mhs_baru_transfer=int(to_clean_float(row.get('Maba Transfer'))),
                            mhs_aktif_reguler=int(to_clean_float(row.get('Mhs Aktif Reguler'))),
                            mhs_aktif_transfer=int(to_clean_float(row.get('Mhs Aktif Transfer')))
                        )
                    logs.append("Tabel 2a")

                # --- PROSES TABEL 3A (DOSEN TETAP) ---
                # Menggunakan field 'nidk' sesuai permintaan
                s3a = next((s for s in sheet_names if '3a' in s.lower() or 'dosen' in s.lower()), None)
                if s3a:
                    df3 = pd.read_excel(xls, s3a)
                    df3.columns = [str(c).strip() for c in df3.columns]
                    DosenTetap.objects.all().delete()
                    for _, row in df3.iterrows():
                        DosenTetap.objects.create(
                            nama_dosen=str(row.get('Nama Dosen', '')),
                            nidk=str(row.get('NIDN / NIDK', row.get('NIDK', ''))), # Mapping ke nidk
                            magister=str(row.get('Magister', '')),
                            doktor=str(row.get('Doktor', '')),
                            bidang_keahlian=str(row.get('Bidang Keahlian', '')),
                            jabatan_akademik=str(row.get('Jabatan Akademik', '')),
                            sertifikat_pendidik=str(row.get('Sertifikat Pendidik', '')),
                            matkul_diampu=str(row.get('Mata Kuliah diampu', ''))
                        )
                    logs.append("Tabel 3a")

                # --- PROSES TABEL 4 (PENGGUNAAN DANA) ---
                s4 = next((s for s in sheet_names if '4' in s.lower() or 'dana' in s.lower()), None)
                if s4:
                    df = pd.read_excel(xls, s4)
                    df.columns = [str(c).strip() for c in df.columns]
                    PenggunaanDana.objects.all().delete()
                    for _, row in df.iterrows():
                        if pd.notna(row.get('Jenis Penggunaan')):
                            PenggunaanDana.objects.create(
                                jenis_penggunaan=str(row.get('Jenis Penggunaan')),
                                ts_2=to_clean_float(row.get('TS-2')),
                                ts_1=to_clean_float(row.get('TS-1')),
                                ts=to_clean_float(row.get('TS'))
                            )
                    logs.append("Tabel 4")
            return JsonResponse({'status': 'success', 'message': f'Berhasil: {", ".join(logs)}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

# --- 2. LOGIKA VIEW TABEL & AUTOSAVE (CRUD MANUAL) ---

def tabel_2a(request):
    """View Tabel 2a: Sinkronisasi 8 Kolom Mahasiswa"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        tahun = request.POST.getlist('tahun_akademik[]')
        daya = request.POST.getlist('daya_tampung[]')
        pendaftar = request.POST.getlist('pendaftar[]')
        lulus = request.POST.getlist('lulus_seleksi[]')
        reg_maba = request.POST.getlist('mhs_baru_reguler[]')
        trf_maba = request.POST.getlist('mhs_baru_transfer[]')
        reg_aktif = request.POST.getlist('mhs_aktif_reguler[]')
        trf_aktif = request.POST.getlist('mhs_aktif_transfer[]')

        with transaction.atomic():
            DataMahasiswa.objects.all().delete()
            for i in range(len(tahun)):
                if tahun[i].strip():
                    DataMahasiswa.objects.create(
                        tahun_akademik=tahun[i], 
                        daya_tampung=int(daya[i] or 0),
                        pendaftar=int(pendaftar[i] or 0),
                        lulus_seleksi=int(lulus[i] or 0),
                        mhs_baru_reguler=int(reg_maba[i] or 0),
                        mhs_baru_transfer=int(trf_maba[i] or 0),
                        mhs_aktif_reguler=int(reg_aktif[i] or 0),
                        mhs_aktif_transfer=int(trf_aktif[i] or 0)
                    )
        return JsonResponse({'status': 'success'})
    data = DataMahasiswa.objects.all().order_by('id')
    return render(request, 'core/tabel_2a.html', {'data': data})

def tabel_3a(request):
    """View Tabel 3a: Mendukung Autosave & Tombol Delete (Menggunakan 'nidk')"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        nama = request.POST.getlist('nama_dosen[]')
        nidk_list = request.POST.getlist('nidk[]') # Mengambil list nidk
        magister = request.POST.getlist('magister[]')
        doktor = request.POST.getlist('doktor[]')
        bidang = request.POST.getlist('bidang_keahlian[]')
        jabatan = request.POST.getlist('jabatan_akademik[]')
        sertifikat = request.POST.getlist('sertifikat_pendidik[]')
        matkul = request.POST.getlist('matkul_diampu[]')

        with transaction.atomic():
            DosenTetap.objects.all().delete() # Hapus semua agar sinkron dengan layar (Fitur Delete)
            for i in range(len(nama)):
                if nama[i].strip():
                    DosenTetap.objects.create(
                        nama_dosen=nama[i],
                        nidk=nidk_list[i], # Menggunakan field 'nidk'
                        magister=magister[i],
                        doktor=doktor[i],
                        bidang_keahlian=bidang[i],
                        jabatan_akademik=jabatan[i],
                        sertifikat_pendidik=sertifikat[i],
                        matkul_diampu=matkul[i]
                    )
        return JsonResponse({'status': 'success'})
    data = DosenTetap.objects.all().order_by('id')
    return render(request, 'core/tabel_3a.html', {'data': data})

# --- 2. VIEW TABEL 4 (SINKRONISASI MANUAL & TAMPILAN) ---
def tabel_4(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        jenis = request.POST.getlist('jenis_penggunaan[]')
        ts2 = request.POST.getlist('ts_2[]')
        ts1 = request.POST.getlist('ts_1[]')
        ts = request.POST.getlist('ts[]')
        
        with transaction.atomic():
            PenggunaanDana.objects.all().delete()
            for i in range(len(jenis)):
                if jenis[i].strip():
                    PenggunaanDana.objects.create(
                        jenis_penggunaan=jenis[i],
                        ts_2=to_clean_float(ts2[i]), 
                        ts_1=to_clean_float(ts1[i]), 
                        ts=to_clean_float(ts[i])
                    )
        return JsonResponse({'status': 'success'})

    data = PenggunaanDana.objects.all().order_by('id')
    # Default label supaya tabel tidak kosong saat pertama kali dibuka
    default_labels = [
        "Biaya Operasional Pendidikan", 
        "Biaya Penelitian", 
        "Biaya Pengabdian kepada Masyarakat (PkM)", 
        "Biaya Investasi"
    ]
    return render(request, 'core/tabel_4.html', {'data': data, 'default_labels': default_labels})

#--- Tabel 5_1 ---#
def tabel_5_1(request):
    """View untuk menampilkan dan menyimpan data Tabel 5.1 secara otomatis."""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Mengambil data list dari form
        jenis_list = request.POST.getlist('jenis_tata_kelola[]')
        nama_list = request.POST.getlist('nama_sistem[]')
        akses_list = request.POST.getlist('akses[]')
        unit_list = request.POST.getlist('unit_pengelola[]')

        with transaction.atomic():
            # Sinkronisasi penuh: Hapus data lama dan simpan baris yang baru
            SistemTataKelola.objects.all().delete()
            for i in range(len(nama_list)):
                # Hanya simpan jika nama sistem diisi (menghindari baris kosong)
                if nama_list[i].strip():
                    SistemTataKelola.objects.create(
                        jenis_tata_kelola=jenis_list[i],
                        nama_sistem=nama_list[i],
                        akses=akses_list[i],
                        unit_pengelola=unit_list[i]
                    )
        return JsonResponse({'status': 'success'})

    # Ambil data yang tersimpan untuk ditampilkan kembali di tabel
    data = SistemTataKelola.objects.all().order_by('id')
    return render(request, 'core/tabel_5_1.html', {'data': data})

# --- 3. VIEW IDENTITAS (PASTIKAN TETAP ADA) ---
def identitas_pengusul(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        IdentitasPengusul.objects.update_or_create(
            id=1,
            defaults={
                'perguruan_tinggi': request.POST.get('perguruan_tinggi'),
                'unit_pengelola': request.POST.get('unit_pengelola'),
                'program_studi': request.POST.get('program_studi'),
                'email': request.POST.get('email'),
                'telepon': request.POST.get('telepon'),
                'website': request.POST.get('website'),
                'kota_pendirian': request.POST.get('kota_pendirian'),
            }
        )
        return JsonResponse({'status': 'success'})
    return render(request, 'core/sampul.html', {'identitas': IdentitasPengusul.objects.first()})
    # Ambil data dari DB
    data = PenggunaanDana.objects.all().order_by('id')
    
    # Label default jika database masih kosong
    default_labels = [
        "Biaya Operasional Pendidikan",
        "Biaya Penelitian",
        "Biaya Pengabdian kepada Masyarakat (PkM)",
        "Biaya Investasi (SDM, Sarpras, dsb)"
    ]
    
    return render(request, 'core/tabel_4.html', {
        'data': data, 
        'default_labels': default_labels
    })

# --- 3. DASHBOARD, WORD EXPORT, & PLACEHOLDERS ---

def dashboard(request): return render(request, 'core/dashboard.html')
def tabel_1(request): return render(request, 'core/tabel_1.html', {'data': Tabel1Kerjasama.objects.all()})
def identitas_pengusul(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        with transaction.atomic():
            IdentitasPengusul.objects.update_or_create(
                id=1,
                defaults={
                    'perguruan_tinggi': request.POST.get('perguruan_tinggi'),
                    'unit_pengelola': request.POST.get('unit_pengelola'),
                    'program_studi': request.POST.get('program_studi'), # Sekarang sinkron
                    'jenis_program': request.POST.get('jenis_program'),
                    'alamat': request.POST.get('alamat'),
                    'telepon': request.POST.get('telepon'), # Nama sudah sama
                    'email': request.POST.get('email'),     # Sudah dipisah
                    'website': request.POST.get('website'), # Sudah dipisah
                    'kota_pendirian': request.POST.get('kota_pendirian'),
                }
            )
        return JsonResponse({'status': 'success'})
    
    identitas = IdentitasPengusul.objects.first()
    return render(request, 'core/sampul.html', {'identitas': identitas})
def generate_word_lkps(request):
    """Export Word terintegrasi untuk semua data terbaru di PostgreSQL"""
    path_template = os.path.join('core', 'static', 'core', 'templates_word', 'template_lkps.docx')
    if not os.path.exists(path_template): return HttpResponse("Template tidak ditemukan", status=404)
    doc = DocxTemplate(path_template)
    konteks = {
        'tabel2a': DataMahasiswa.objects.all().order_by('id'), 
        'tabel3a': DosenTetap.objects.all().order_by('id'),
        'tabel4': PenggunaanDana.objects.all().order_by('id')
    }
    doc.render(konteks)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=LKPS_Universitas_Pradita.docx'
    return response

# Placeholders (Agar navigasi tidak Error 404/AttributeError)
def tim_penyusun(request): return render(request, 'core/tim_penyusun.html')
def input_penelitian(request): return render(request, 'core/input_penelitian.html', {'data': PenelitianDTPR.objects.all()})
def tabel_5_2(request): return render(request, 'core/tabel_5_2.html')
def tabel_6(request): return render(request, 'core/tabel_6.html')
def tabel_7(request): return render(request, 'core/tabel_7.html')
def tabel_8(request): return render(request, 'core/tabel_8.html')
def tabel_9(request): return render(request, 'core/tabel_9.html')