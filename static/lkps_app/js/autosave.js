// Fungsi global yang bisa dipanggil darimana saja
function showToast(message, type = 'success') {
    const toastEl = document.getElementById('liveToast');
    const toastMessage = document.getElementById('toast-message');
    
    // Ubah warna berdasarkan tipe
    toastEl.className = `toast align-items-center text-bg-${type} border-0`;
    
    let icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    toastMessage.innerHTML = `<i class="fas ${icon} me-2"></i> ${message}`;
    
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

// Simulasi Loading Generate Word (Bisa ditaruh di onclick button generate)
function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    overlay.classList.remove('d-none');
    
    // Simulasi loading 3 detik, lalu sembunyikan (Nanti diganti saat backend siap)
    setTimeout(() => {
        overlay.classList.add('d-none');
        showToast('Dokumen Word berhasil dibuat!', 'success');
    }, 3000);
}