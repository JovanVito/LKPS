# dummy_excel.py
import pandas as pd

# Data Pendanaan (Tabel 1.A.2) [cite: 103, 104]
data_dana = {
    'Sumber Pendanaan': ['Mahasiswa (SPP)', 'Yayasan', 'Pemerintah'],
    'TS-2': [5000, 2000, 1000],
    'TS-1': [5500, 2100, 1100],
    'TS': [6000, 2200, 1200],
    'Link Bukti': ['http://drive.google.com/bukti1', '', '']
}

# Data Tenaga Kependidikan (Tabel 1.A.5) [cite: 130, 129]
data_sdm = {
    'Jenis Tenaga': ['Pustakawan', 'Laboran', 'Administrasi'],
    'S3': [0, 0, 0],
    'S2': [1, 1, 2],
    'S1': [2, 3, 5],
    'Unit Kerja': ['Perpustakaan', 'Lab Informatika', 'TU Fakultas']
}

# Data Mahasiswa (Tabel 2.A.1) [cite: 142, 141]
data_mhs = {
    'Tahun': ['TS-3', 'TS-2', 'TS-1', 'TS'],
    'Daya Tampung': [50, 50, 50, 60],
    'Pendaftar': [120, 135, 150, 180],
    'Lulus Seleksi': [55, 55, 55, 65],
    'Baru Reguler': [48, 50, 52, 60],
    'Aktif Reguler': [180, 190, 200, 220]
}

with pd.ExcelWriter('Data_Dummy_LKPS.xlsx', engine='openpyxl') as writer:
    # Simpan sheet lama (identitas) dan tambahkan yang baru
    pd.DataFrame(data_dana).to_excel(writer, sheet_name='1A2_Pendanaan', index=False)
    pd.DataFrame(data_sdm).to_excel(writer, sheet_name='1A5_SDM', index=False)
    pd.DataFrame(data_mhs).to_excel(writer, sheet_name='2A1_Mahasiswa', index=False)

print("Excel Dummy Berhasil Diperbarui!")