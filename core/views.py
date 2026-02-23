import os
import io
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from docxtpl import DocxTemplate
from .models import IdentitasPengusul, SumberPendanaan, DataMahasiswa

def home(request):
    return render(request, 'core/index.html')

def export_to_word(request):
    # 1. Tentukan jalur template secara absolut
    template_path = os.path.join(settings.BASE_DIR, 'template_lkps.docx')
    
    # Cek apakah file template benar-benar ada
    if not os.path.exists(template_path):
        return HttpResponse(f"Error: File '{template_path}' tidak ditemukan. Jalankan 'python generate_template.py' dulu!")

    # 2. Ambil data dari PostgreSQL
    # Mengambil Identitas Pengusul [cite: 58]
    identitas = IdentitasPengusul.objects.first()
    
    if not identitas:
        return HttpResponse("Error: Data Identitas masih kosong di Database. Isi dulu lewat Django Admin!")

    # 3. Load Template
    doc = DocxTemplate(template_path)

    # 4. Siapkan Context (Mapping Data ke Tag Word)
    context = {
        # Data Identitas [cite: 58]
        'pt': identitas.perguruan_tinggi,
        'upps': identitas.unit_pengelola,
        'jenis_program': identitas.jenis_program,
        'nama_prodi': identitas.nama_program_studi.nama_prodi,
        'alamat': identitas.alamat,
        'nomor_telepon': identitas.nomor_telepon,
        'email_website': identitas.email_website,
        'sk_pendirian': identitas.nomor_sk_pendirian,
        'akreditasi': identitas.peringkat_akreditasi,

        # Data Tabel 1.A.2 Sumber Pendanaan [cite: 104]
        'dana': [
            {'sumber': d.sumber, 'ts2': d.ts_2, 'ts1': d.ts_1, 'ts': d.ts, 'link': d.link_bukti} 
            for d in SumberPendanaan.objects.all()
        ],

        # Data Tabel 2.A.1 Data Mahasiswa [cite: 141, 142]
        'mahasiswa': [
            {'thn': m.tahun_akademik, 'daya': m.daya_tampung, 'daftar': m.pendaftar, 
             'lulus': m.lulus_seleksi, 'baru': m.mhs_baru_reguler, 'aktif': m.mhs_aktif_reguler}
            for m in DataMahasiswa.objects.all()
        ],
    }

    # 5. Render & Kirim Response
    try:
        doc.render(context)
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename=Hasil_LKPS_LAM_INFOKOM.docx'
        return response
    except Exception as e:
        return HttpResponse(f"Terjadi kesalahan saat render: {str(e)}")