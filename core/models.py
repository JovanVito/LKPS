from django.db import models

# --- DATA MASTER ---
class ProgramStudi(models.Model):
    nama_prodi = models.CharField(max_length=100)
    fakultas = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama_prodi

from django.db import models

class ProgramStudi(models.Model): # Jika kamu masih pakai tabel ini
    nama = models.CharField(max_length=100)
    def __str__(self): return self.nama

class IdentitasPengusul(models.Model):
    perguruan_tinggi = models.CharField(max_length=200, default="Universitas Pradita")
    unit_pengelola = models.CharField(max_length=200, blank=True, null=True)
    jenis_program = models.CharField(max_length=100, default="Sarjana")
    
    # KUNCI: Gunakan CharField agar dropdown teks langsung tersimpan
    program_studi = models.CharField(max_length=100, blank=True, null=True) 
    
    kota_pendirian = models.CharField(max_length=100, default="Tangerang")
    alamat = models.TextField(blank=True, null=True)
    
    # Nama field disamakan dengan view/HTML
    telepon = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    
    # Field SK dan Akreditasi
    nomor_sk_pendirian = models.CharField(max_length=100, blank=True, null=True)
    tanggal_sk_pendirian = models.DateField(blank=True, null=True)
    pejabat_sk_pendirian = models.CharField(max_length=100, blank=True, null=True)
    tahun_pertama_menerima = models.IntegerField(blank=True, null=True)
    peringkat_akreditasi = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.perguruan_tinggi} - {self.program_studi}"

# --- TABEL 1: KERJASAMA ---
class Tabel1Kerjasama(models.Model):
    lembaga_mitra = models.CharField(max_length=255)
    tingkat = models.CharField(max_length=50) 
    judul_kegiatan = models.TextField()
    manfaat = models.TextField()
    durasi = models.CharField(max_length=50)

    def __str__(self):
        return self.lembaga_mitra


# --- TABEL 2.A: SELEKSI MAHASISWA BARU ---
class DataMahasiswa(models.Model):
    tahun_akademik = models.CharField(max_length=10)
    daya_tampung = models.IntegerField(default=0)
    pendaftar = models.IntegerField(default=0)
    lulus_seleksi = models.IntegerField(default=0)
    mhs_baru_reguler = models.IntegerField(default=0)
    mhs_baru_transfer = models.IntegerField(default=0)
    mhs_aktif_reguler = models.IntegerField(default=0)
    mhs_aktif_transfer = models.IntegerField(default=0)

    def __str__(self):
        return self.tahun_akademik


# --- TABEL 3.A.1: DOSEN TETAP (BARU) ---
class DosenTetap(models.Model):
    JABATAN_CHOICES = [
        ('Tenaga Pengajar', 'Tenaga Pengajar'),
        ('Asisten Ahli', 'Asisten Ahli'),
        ('Lektor', 'Lektor'),
        ('Lektor Kepala', 'Lektor Kepala'),
        ('Guru Besar', 'Guru Besar'),
    ]
    nama_dosen = models.CharField(max_length=255)
    nidk = models.CharField(max_length=50)
    magister = models.CharField(max_length=255, blank=True, null=True)
    doktor = models.CharField(max_length=255, blank=True, null=True)
    bidang_keahlian = models.CharField(max_length=255)
    jabatan_akademik = models.CharField(max_length=100, choices=JABATAN_CHOICES)
    sertifikat_pendidik = models.CharField(max_length=255, blank=True, null=True)
    matkul_diampu = models.TextField()

    def __str__(self):
        return self.nama_dosen


# --- TABEL 3.A.2: PENELITIAN DTPR ---
class PenelitianDTPR(models.Model):
    SUMBER_CHOICES = [
        ('Mandiri', 'Mandiri'),
        ('PT', 'Perguruan Tinggi'),
        ('Nasional', 'Nasional'),
        ('Internasional', 'Internasional'),
    ]
    sumber_pembiayaan = models.CharField(max_length=100, choices=SUMBER_CHOICES)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    jumlah = models.IntegerField(default=0, blank=True)

    def save(self, *args, **kwargs):
        self.jumlah = self.ts_2 + self.ts_1 + self.ts
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sumber_pembiayaan

# --- TABEL 4 Penggunaan Dana ---
class PenggunaanDana(models.Model):
    jenis_penggunaan = models.CharField(max_length=255)
    ts_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    rata_rata = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)

    def save(self, *args, **kwargs):
        self.rata_rata = (self.ts_2 + self.ts_1 + self.ts) / 3
        super().save(*args, **kwargs)

        # --- TABEL 5.A: KURIKULUM, CAPAIAN, DAN RENCANA PEMBELAJARAN ---
class Kurikulum(models.Model):
    semester = models.IntegerField(default=1)
    kode_matkul = models.CharField(max_length=20)
    nama_matkul = models.CharField(max_length=255)
    matkul_kompetensi = models.BooleanField(default=False) # Checkbox: Ya/Tidak
    sks_kuliah = models.IntegerField(default=0)
    sks_seminar = models.IntegerField(default=0)
    sks_praktikum = models.IntegerField(default=0)
    jam_kredit = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Capaian Pembelajaran (CPL)
    capaian_sikap = models.BooleanField(default=False)
    capaian_pengetahuan = models.BooleanField(default=False)
    capaian_keterampilan_umum = models.BooleanField(default=False)
    capaian_keterampilan_khusus = models.BooleanField(default=False)
    
    dokumen_rencana_pembelajaran = models.CharField(max_length=255, blank=True, null=True)
    unit_penyelenggara = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.kode_matkul} - {self.nama_matkul}"
# --- LAIN-LAIN (SUMBER DANA & KEPENDIDIKAN) ---
class SumberPendanaan(models.Model):
    sumber = models.CharField(max_length=200)
    ts_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    jumlah = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    link_bukti = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.jumlah = self.ts_2 + self.ts_1 + self.ts
        super().save(*args, **kwargs)

class TenagaKependidikan(models.Model):
    jenis_tenaga = models.CharField(max_length=100)
    jenjang_s3 = models.IntegerField(default=0)
    jenjang_s2 = models.IntegerField(default=0)
    jenjang_s1 = models.IntegerField(default=0)
    unit_kerja = models.CharField(max_length=100)

class PublikasiMahasiswa(models.Model):
    jenis_publikasi = models.CharField(max_length=200)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    jumlah = models.IntegerField(default=0, blank=True)

    def save(self, *args, **kwargs):
        self.jumlah = self.ts_2 + self.ts_1 + self.ts
        super().save(*args, **kwargs)
    
class SistemTataKelola(models.Model):
    JENIS_CHOICES = [
        ('Pendidikan', 'Pendidikan'),
        ('Keuangan', 'Keuangan'),
        ('SDM', 'SDM'),
        ('Sarana Prasarana', 'Sarana Prasarana'),
        ('Lainnya', 'Lainnya'),
    ]
    AKSES_CHOICES = [
        ('Internet', 'Internet'),
        ('Lokal', 'Lokal'),
    ]

    jenis_tata_kelola = models.CharField(max_length=100, choices=JENIS_CHOICES)
    nama_sistem = models.CharField(max_length=255)
    akses = models.CharField(max_length=50, choices=AKSES_CHOICES)
    unit_pengelola = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nama_sistem} ({self.jenis_tata_kelola})"