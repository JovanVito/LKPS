# lkps_app/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
# ==========================================
# MODEL MASTER (Tabel Referensi)
# ==========================================

class ProgramStudi(models.Model):
    nama_prodi = models.CharField(max_length=100, unique=True)
    jenjang_studi = models.CharField(max_length=100)
    akreditasi = models.CharField(max_length=50)
    no_sk = models.CharField(max_length=100)

class ProfilPengguna(models.Model):
    # Menyambungkan tabel ini dengan tabel User bawaan Django (One-to-One)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    nomor_induk = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50)
    akses_prodi = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} - {self.role}"
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
    program_studi = models.OneToOneField(ProgramStudi, on_delete=models.CASCADE, related_name='identitas_pengusul')
    logo_pt = models.ImageField(upload_to='logo/', null=True, blank=True)

    # Field Halaman Muka
    nama_ps_sampul = models.CharField(max_length=200, blank=True)
    nama_pt_sampul = models.CharField(max_length=200, blank=True)
    kota_sampul = models.CharField(max_length=100, blank=True)
    tahun_sampul = models.IntegerField(default=2026)
    
    # Field Identitas Pengusul
    unit_pengelola = models.CharField(max_length=200, blank=True)
    perguruan_tinggi = models.CharField(max_length=200, blank=True)
    alamat = models.TextField(blank=True)
    telepon = models.CharField(max_length=50, blank=True)
    email_web = models.CharField(max_length=200, blank=True)
    sk_pt = models.CharField(max_length=100, blank=True)
    tgl_sk_pt = models.DateField(null=True, blank=True)
    sk_ps = models.CharField(max_length=100, blank=True)
    tgl_sk_ps = models.DateField(null=True, blank=True)

class TimPenyusun(models.Model):
    identitas = models.ForeignKey(IdentitasPengusul, on_delete=models.CASCADE, related_name='tim_penyusun')
    nama = models.CharField(max_length=200, blank=True)
    nidn = models.CharField(max_length=50, blank=True)
    jabatan = models.CharField(max_length=100, blank=True)
    tanggal_pengisian = models.DateField(null=True, blank=True)
    # UBAH KE ImageField agar bisa diatur ukurannya nanti di laporan
    tanda_tangan = models.ImageField(upload_to='ttd_penyusun/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tim Penyusun"
# class Tabel 
class Tabel_1A1(models.Model):
    unit_kerja = models.CharField(max_length=255)
    nama_ketua = models.CharField(max_length=255)
    periode_jabatan = models.CharField(max_length=100)
    pendidikan_terakhir = models.CharField(max_length=50)
    jabatan_fungsional = models.CharField(max_length=100)
    tupoksi = models.TextField() # Untuk deskripsi tugas yang panjang

    def __str__(self):
        return f"{self.unit_kerja} - {self.nama_ketua}"

    class Meta:
        verbose_name = "Tabel 1.A.1 Pimpinan & Tupoksi"

class Tabel_1A2_Sumber(models.Model):
    sumber_dana = models.CharField(max_length=255)
    ts_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_1A3_Penggunaan(models.Model):
    penggunaan = models.CharField(max_length=255)
    ts_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_1A4(models.Model):
    nama_dosen = models.CharField(max_length=255)
    sks_ps_sendiri = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_ps_lain = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_pt_lain = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_penelitian = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_pkm = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_tambahan = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "1.A.4 Beban Kerja DTPR"

class Tabel_1A5(models.Model):
    jenis_tenaga = models.CharField(max_length=255)
    s3 = models.IntegerField(default=0)
    s2 = models.IntegerField(default=0)
    s1 = models.IntegerField(default=0)
    d3 = models.IntegerField(default=0)
    d2_d1 = models.IntegerField(default=0)
    sma_smk = models.IntegerField(default=0)
    unit_kerja = models.CharField(max_length=255)

    class Meta:
        verbose_name = "1.A.5 Tenaga Kependidikan"

# --- KRITERIA 2: MAHASISWA & LULUSAN ---
class Tabel_2A_Mahasiswa(models.Model):
    tahun_akademik = models.CharField(max_length=20)
    daya_tampung = models.IntegerField(default=0)
    pendaftar = models.IntegerField(default=0)
    lulus_seleksi = models.IntegerField(default=0)
    mhs_baru_reguler = models.IntegerField(default=0)
    mhs_baru_transfer = models.IntegerField(default=0)
    total_mhs_reguler = models.IntegerField(default=0)
    total_mhs_transfer = models.IntegerField(default=0)

    class Meta:
        verbose_name = "2.A Data Mahasiswa"

class Tabel_2A2_Asal(models.Model):
    asal_mahasiswa = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    link_bukti = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "2.A.2 Keragaman Asal"

class Tabel_2A3_Kondisi(models.Model):
    status = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "2.A.3 Kondisi Jumlah"

class Tabel_2B1_MK(models.Model):
    nama_mk = models.CharField(max_length=255)
    sks = models.IntegerField(default=0)
    semester = models.IntegerField(default=0)
    pl1 = models.BooleanField(default=False)
    pl2 = models.BooleanField(default=False)
    pl3 = models.BooleanField(default=False)
    pl4 = models.BooleanField(default=False)

class Tabel_2B2_CPL(models.Model):
    kode_cpl = models.CharField(max_length=100)
    pl1 = models.BooleanField(default=False)
    pl2 = models.BooleanField(default=False)
    pl3 = models.BooleanField(default=False)
    pl4 = models.BooleanField(default=False)

class Tabel_2B3_Pemenuhan(models.Model):
    cpl = models.CharField(max_length=100)
    cpmk = models.CharField(max_length=100)
    smt1 = models.CharField(max_length=100, blank=True)
    smt2 = models.CharField(max_length=100, blank=True)
    smt3 = models.CharField(max_length=100, blank=True)

class Tabel_2B4_MasaTunggu(models.Model):
    tahun_lulus = models.CharField(max_length=20)
    jml_lulusan = models.IntegerField(default=0)
    jml_terlacak = models.IntegerField(default=0)
    waktu_tunggu = models.DecimalField(max_digits=5, decimal_places=1, default=0)

class Tabel_2B5_BidangKerja(models.Model):
    tahun_lulus = models.CharField(max_length=20)
    jml_lulusan = models.IntegerField(default=0)
    jml_terlacak = models.IntegerField(default=0)
    bidang_infokom = models.IntegerField(default=0)
    bidang_non_infokom = models.IntegerField(default=0)
    tingkat_multinasional = models.IntegerField(default=0)
    tingkat_nasional = models.IntegerField(default=0)
    tingkat_wirausaha = models.IntegerField(default=0)

class Tabel_2B6_Kepuasan(models.Model):
    jenis_kemampuan = models.CharField(max_length=255)
    sangat_baik = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    baik = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    cukup = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    kurang = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    tindak_lanjut = models.TextField(blank=True, null=True)

class Tabel_2B_Summary(models.Model):
    total_alumni_3thn = models.IntegerField(default=0)
    total_responden = models.IntegerField(default=0)
    total_mhs_aktif_ts = models.IntegerField(default=0)

# --- KRITERIA 3 & 4: PENELITIAN & PKM ---
# --- KRITERIA 3: PENELITIAN & SARPAS ---
class Tabel_3A1_Sarana(models.Model):
    nama_prasarana = models.CharField(max_length=255)
    daya_tampung = models.IntegerField(default=0)
    luas_ruang = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    kepemilikan = models.CharField(max_length=50) # M / W
    lisensi = models.CharField(max_length=50) # L / P / Tidak Berlisensi
    perangkat = models.TextField(blank=True, null=True)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_3A2_Penelitian(models.Model):
    nama_dtpr = models.CharField(max_length=255)
    jml_mhs = models.IntegerField(default=0)
    judul = models.TextField()
    jenis_hibah = models.CharField(max_length=255)
    sumber_lni = models.CharField(max_length=10) # L/N/I
    durasi = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    dana_ts2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_3C1_Kerjasama(models.Model):
    judul = models.TextField()
    mitra = models.CharField(max_length=255)
    sumber_lni = models.CharField(max_length=10) # L/N/I
    durasi = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    dana_ts2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_3C2_Publikasi(models.Model):
    nama_dtpr = models.CharField(max_length=255)
    judul = models.TextField()
    jenis_pub = models.CharField(max_length=50)
    ts2 = models.BooleanField(default=False)
    ts1 = models.BooleanField(default=False)
    ts = models.BooleanField(default=False)

class Tabel_3C3_HKI(models.Model):
    judul = models.TextField()
    jenis_hki = models.CharField(max_length=255)
    nama_dtpr = models.CharField(max_length=255)
    ts2 = models.BooleanField(default=False)
    ts1 = models.BooleanField(default=False)
    ts = models.BooleanField(default=False)

class Tabel_3_Summary(models.Model):
    link_roadmap = models.URLField(blank=True, null=True)
    total_jenis_hibah = models.IntegerField(default=0)
    total_mitra = models.IntegerField(default=0)

# --- KRITERIA 4: PENGABDIAN KEPADA MASYARAKAT (PkM) ---
class Tabel_4A1_Sarana(models.Model):
    nama_prasarana = models.CharField(max_length=255)
    daya_tampung = models.IntegerField(default=0)
    luas_ruang = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    kepemilikan = models.CharField(max_length=50) # M / W
    lisensi = models.CharField(max_length=50) # L / P / T
    perangkat = models.TextField(blank=True, null=True)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_4A2_PkM(models.Model):
    nama_dtpr = models.CharField(max_length=255)
    judul = models.TextField()
    jml_mhs = models.IntegerField(default=0)
    jenis_hibah = models.CharField(max_length=255)
    sumber_lni = models.CharField(max_length=10) # L/N/I
    durasi = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    dana_ts2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_4C1_Kerjasama(models.Model):
    judul = models.TextField()
    mitra = models.CharField(max_length=255)
    sumber_lni = models.CharField(max_length=10) # L/N/I
    durasi = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    dana_ts2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_4C2_Diseminasi(models.Model):
    nama_dtpr = models.CharField(max_length=255)
    judul = models.TextField()
    lni = models.CharField(max_length=10) # L/N/I
    ts2 = models.BooleanField(default=False)
    ts1 = models.BooleanField(default=False)
    ts = models.BooleanField(default=False)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_4C3_HKI(models.Model):
    judul = models.TextField()
    jenis_hki = models.CharField(max_length=255)
    nama_dtpr = models.CharField(max_length=255)
    ts2 = models.BooleanField(default=False)
    ts1 = models.BooleanField(default=False)
    ts = models.BooleanField(default=False)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_4_Summary(models.Model):
    link_roadmap = models.URLField(blank=True, null=True)
    total_jenis_hibah = models.IntegerField(default=0)
    jml_disem_hasil = models.IntegerField(default=0)

# --- KRITERIA 5: AKUNTABILITAS (TATA KELOLA & SARPAS) ---
class Tabel_5_1_TataKelola(models.Model):
    jenis_tata_kelola = models.CharField(max_length=255)
    nama_sistem = models.CharField(max_length=255, blank=True, null=True)
    akses = models.CharField(max_length=50, blank=True, null=True) # Internet / Lokal
    unit_pengelola = models.CharField(max_length=255, blank=True, null=True)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_5_2_Sarana(models.Model):
    nama_prasarana = models.CharField(max_length=255)
    daya_tampung = models.IntegerField(default=0)
    luas_ruang = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    kepemilikan = models.CharField(max_length=50) # M / W
    lisensi = models.CharField(max_length=50) # L / P / Tidak berlisensi
    perangkat = models.TextField(blank=True, null=True)
    link_bukti = models.URLField(blank=True, null=True)

# --- KRITERIA 6: VISI MISI ---
class Tabel_6_Misi(models.Model):
    visi_pt = models.TextField(blank=True, null=True)
    visi_upps = models.TextField(blank=True, null=True)
    visi_ps = models.TextField(blank=True, null=True)
    misi_pt = models.TextField(blank=True, null=True)
    misi_upps = models.TextField(blank=True, null=True)