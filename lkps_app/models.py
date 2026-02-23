# lkps_app/models.py
from django.db import models
from django.utils import timezone

# ==========================================
# MODEL MASTER (Tabel Referensi)
# ==========================================

class ProgramStudi(models.Model):
    """
    Tabel master untuk menyimpan daftar Program Studi di Pradita.
    Tabel lain akan berelasi (ForeignKey) ke tabel ini.
    """
    nama_prodi = models.CharField(max_length=100, unique=True)
    # Bisa ditambahkan kode_prodi, jenjang (S1/D3), dll jika perlu

    def __str__(self):
        return self.nama_prodi
    
    class Meta:
        verbose_name_plural = "Master Program Studi"


# ==========================================
# MODEL DATA LKPS
# ==========================================

# Class abstrak agar kita tidak perlu menulis ulang kolom waktu_resmi di setiap tabel
class TimeStampedModel(models.Model):
    """
    Class abstrak yang menyediakan field waktu_resmi otomatis
    sesuai requirements Excel.
    """
    waktu_resmi = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) # Waktu dibuat
    updated_at = models.DateTimeField(auto_now=True)     # Waktu terakhir diupdate (auto-save)

    class Meta:
        abstract = True


class IdentitasPengusul(TimeStampedModel):
    """
    Model untuk menyimpan data Halaman Sampul / Identitas.
    Relasi: OneToOne (Satu Prodi hanya punya satu data Identitas di satu periode)
    """
    # Menghubungkan data ini ke Prodi tertentu
    program_studi = models.OneToOneField(
        ProgramStudi, 
        on_delete=models.CASCADE,
        related_name='identitas_pengusul'
    )
    
    # Field sesuai PDF Halaman Sampul
    unit_pengelola = models.CharField(max_length=200, help_text="Nama Fakultas/Sekolah Tinggi")
    perguruan_tinggi = models.CharField(max_length=200, default="Universitas Pradita")
    kota_pendirian = models.CharField(max_length=100, default="Tangerang")
    # Tanggal di PDF biasanya otomatis saat print, tapi kita sediakan fieldnya
    tanggal_dokumen = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Identitas LKPS - {self.program_studi.nama_prodi}"
    
    class Meta:
        verbose_name_plural = "Data Identitas Pengusul"