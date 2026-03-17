// ==========================================
// 1. FUNGSI NOTIFIKASI (Kodingan Jovan)
// ==========================================
function showToast(message, type = 'success') {
    const toastEl = document.getElementById('liveToast');
    const toastMessage = document.getElementById('toast-message');
    
    // Ubah warna berdasarkan tipe (success, danger, warning)
    toastEl.className = `toast align-items-center text-bg-${type} border-0`;
    
    let icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    toastMessage.innerHTML = `<i class="fas ${icon} me-2"></i> ${message}`;
    
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    overlay.classList.remove('d-none');
    
    // Nanti diintegrasikan dengan fungsi Generate Word kamu
    setTimeout(() => {
        overlay.classList.add('d-none');
        showToast('Dokumen Word berhasil dibuat!', 'success');
    }, 3000);
}

// ==========================================
// 2. LOGIKA AUTOSAVE DENGAN DEBOUNCING
// ==========================================
let debounceTimer;

// Event listener untuk mendeteksi ketikan di input
document.addEventListener('input', function(e) {
    // Jalankan hanya jika elemen memiliki class 'auto-save-input'
    if (e.target.classList.contains('auto-save-input')) {
        
        clearTimeout(debounceTimer);

        // Set timer 1 detik: simpan setelah user berhenti mengetik
        debounceTimer = setTimeout(function() {
            autoSaveAction(e.target);
        }, 1000); 
    }
});

function autoSaveAction(inputElement) {
    // Cari form terdekat dari input yang sedang diketik
    const form = inputElement.closest('form');
    if (!form) return;

    const formData = new FormData(form);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Panggil fungsi showToast buatan Jovan
            showToast("Perubahan disimpan otomatis", "success");
        } else {
            showToast("Gagal simpan otomatis: " + data.message, "danger");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast("Koneksi ke server terputus", "danger");
    });
}