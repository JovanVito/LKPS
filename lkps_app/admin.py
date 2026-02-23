from django.contrib import admin
from .models import ProgramStudi, IdentitasPengusul

# Mendaftarkan model agar muncul di halaman Admin
@admin.register(ProgramStudi)
class ProgramStudiAdmin(admin.ModelAdmin):
    list_display = ('nama_prodi',) # Menampilkan kolom nama prodi di tabel admin

@admin.register(IdentitasPengusul)
class IdentitasPengusulAdmin(admin.ModelAdmin):
    list_display = ('program_studi', 'unit_pengelola', 'updated_at')