from django.db import models

# Pastikan nama kelasnya ProgramStudi (P dan S huruf kapital)
class ProgramStudi(models.Model):
    nama_prodi = models.CharField(max_length=100)
    fakultas = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama_prodi

class IdentitasPengusul(models.Model):
    perguruan_tinggi = models.CharField(max_length=200)
    unit_pengelola = models.CharField(max_length=200) # [cite: 57]
    jenis_program = models.CharField(max_length=100, default="Magister") # [cite: 1]
    
    # Hubungan ke tabel ProgramStudi
    nama_program_studi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE) # [cite: 57]
    
    alamat = models.TextField() # [cite: 57]
    nomor_telepon = models.CharField(max_length=50) # [cite: 57]
    email_website = models.CharField(max_length=200) # [cite: 57]
    
    # Data SK Pendirian PT [cite: 57, 61]
    nomor_sk_pendirian = models.CharField(max_length=100)
    tanggal_sk_pendirian = models.DateField()
    pejabat_sk_pendirian = models.CharField(max_length=100)
    
    # Data SK Pembukaan PS [cite: 57, 61]
    nomor_sk_pembukaan = models.CharField(max_length=100)
    tanggal_sk_pembukaan = models.DateField()
    pejabat_sk_pembukaan = models.CharField(max_length=100)
    
    tahun_pertama_menerima = models.IntegerField() # [cite: 57]
    peringkat_akreditasi = models.CharField(max_length=50) # [cite: 57]
    nomor_sk_ban_pt = models.CharField(max_length=100) # [cite: 57]

    def __str__(self):
        return f"{self.perguruan_tinggi} - {self.nama_program_studi}"
    
    # core/models.py

from django.db import models

class ProgramStudi(models.Model):
    nama_prodi = models.CharField(max_length=100)
    fakultas = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama_prodi

class IdentitasPengusul(models.Model):
    perguruan_tinggi = models.CharField(max_length=200)
    unit_pengelola = models.CharField(max_length=200)
    jenis_program = models.CharField(max_length=100, default="Magister")
    nama_program_studi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE)
    alamat = models.TextField()
    nomor_telepon = models.CharField(max_length=50)
    email_website = models.CharField(max_length=200)
    nomor_sk_pendirian = models.CharField(max_length=100)
    tanggal_sk_pendirian = models.DateField()
    pejabat_sk_pendirian = models.CharField(max_length=100)
    nomor_sk_pembukaan = models.CharField(max_length=100)
    tanggal_sk_pembukaan = models.DateField()
    pejabat_sk_pembukaan = models.CharField(max_length=100)
    tahun_pertama_menerima = models.IntegerField()
    peringkat_akreditasi = models.CharField(max_length=50)
    nomor_sk_ban_pt = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.perguruan_tinggi} - {self.nama_program_studi}"

# Tabel 1.A.2: Sumber Pendanaan
class SumberPendanaan(models.Model):
    sumber = models.CharField(max_length=200)
    ts_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

# Tabel 1.A.5: Kualifikasi Tenaga Kependidikan
class TenagaKependidikan(models.Model):
    jenis_tenaga = models.CharField(max_length=100)
    jenjang_s3 = models.IntegerField(default=0)
    jenjang_s2 = models.IntegerField(default=0)
    jenjang_s1 = models.IntegerField(default=0)
    unit_kerja = models.CharField(max_length=100)

# Tabel 2.A.1: Data Mahasiswa
class DataMahasiswa(models.Model):
    tahun_akademik = models.CharField(max_length=10)
    daya_tampung = models.IntegerField()
    pendaftar = models.IntegerField()
    lulus_seleksi = models.IntegerField()
    mhs_baru_reguler = models.IntegerField()
    mhs_aktif_reguler = models.IntegerField()