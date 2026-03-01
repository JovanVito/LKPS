from django.contrib import admin
from .models import (
    ProgramStudi, IdentitasPengusul, Tabel1Kerjasama, 
    SumberPendanaan, TenagaKependidikan, DataMahasiswa, 
    PenelitianDTPR, PublikasiMahasiswa, DosenTetap, PenggunaanDana, Kurikulum, SistemTataKelola
)

# --- KONFIGURASI ADMIN ---

@admin.register(IdentitasPengusul)
class IdentitasPengusulAdmin(admin.ModelAdmin):
    list_display = ('perguruan_tinggi', 'unit_pengelola', 'peringkat_akreditasi')
    search_fields = ('perguruan_tinggi', 'unit_pengelola')

@admin.register(Tabel1Kerjasama)
class Tabel1KerjasamaAdmin(admin.ModelAdmin):
    list_display = ('lembaga_mitra', 'tingkat', 'durasi')
    list_filter = ('tingkat',)

@admin.register(DataMahasiswa)
class DataMahasiswaAdmin(admin.ModelAdmin):
    list_display = ('tahun_akademik', 'daya_tampung', 'pendaftar', 'mhs_baru_reguler')
    list_editable = ('daya_tampung', 'pendaftar', 'mhs_baru_reguler')

@admin.register(PenelitianDTPR)
class PenelitianDTPRAdmin(admin.ModelAdmin):
    list_display = ('sumber_pembiayaan', 'ts_2', 'ts_1', 'ts', 'jumlah')
    readonly_fields = ('jumlah',)

@admin.register(SumberPendanaan)
class SumberPendanaanAdmin(admin.ModelAdmin):
    list_display = ('sumber', 'ts_2', 'ts_1', 'ts', 'jumlah')
    readonly_fields = ('jumlah',)

@admin.register(PublikasiMahasiswa)
class PublikasiMahasiswaAdmin(admin.ModelAdmin):
    list_display = ('jenis_publikasi', 'jumlah')

# Pendaftaran Model (Hanya SATU kali untuk setiap model)
admin.site.register(ProgramStudi)
admin.site.register(TenagaKependidikan)
admin.site.register(DosenTetap)
admin.site.register(PenggunaanDana)
admin.site.register(Kurikulum)
admin.site.register(SistemTataKelola)