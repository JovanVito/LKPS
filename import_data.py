import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lkps_project.settings')
django.setup()

from core.models import ProgramStudi, IdentitasPengusul, SumberPendanaan, TenagaKependidikan, DataMahasiswa

def run_import():
    file_path = 'Data_Dummy_LKPS.xlsx'
    
    # 1. Import Pendanaan
    df_dana = pd.read_excel(file_path, sheet_name='1A2_Pendanaan')
    for _, row in df_dana.iterrows():
        SumberPendanaan.objects.update_or_create(
            sumber=row['Sumber Pendanaan'],
            defaults={'ts_2': row['TS-2'], 'ts_1': row['TS-1'], 'ts': row['TS']}
        )

    # 2. Import Tenaga Kependidikan
    df_sdm = pd.read_excel(file_path, sheet_name='1A5_SDM')
    for _, row in df_sdm.iterrows():
        TenagaKependidikan.objects.update_or_create(
            jenis_tenaga=row['Jenis Tenaga'],
            defaults={'jenjang_s3': row['S3'], 'jenjang_s2': row['S2'], 'jenjang_s1': row['S1'], 'unit_kerja': row['Unit Kerja']}
        )

    # 3. Import Data Mahasiswa
    df_mhs = pd.read_excel(file_path, sheet_name='2A1_Mahasiswa')
    for _, row in df_mhs.iterrows():
        DataMahasiswa.objects.update_or_create(
            tahun_akademik=row['Tahun'],
            defaults={
                'daya_tampung': row['Daya Tampung'],
                'pendaftar': row['Pendaftar'],
                'lulus_seleksi': row['Lulus Seleksi'],
                'mhs_baru_reguler': row['Baru Reguler'],
                'mhs_aktif_reguler': row['Aktif Reguler']
            }
        )
    print("Semua data tabel berhasil diimpor!")

if __name__ == "__main__":
    run_import()