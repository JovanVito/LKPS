// Tambahkan event listener untuk tombol import
document.querySelector('.btn-outline-success').addEventListener('click', function() {
    let input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx, .xls';

    // Trigger klik otomatis agar jendela pilih file terbuka
    input.click();

    input.onchange = function(e) {
        let file = e.target.files[0];
        if (!file) return;

        let formData = new FormData();
        formData.append('file_excel', file);

        // Ambil CSRF Token dari cookie (Standar Django)
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]') ? 
                          document.querySelector('[name=csrfmiddlewaretoken]').value : "";

        console.log("Memulai proses import...");

        fetch('/import_excel_lkps/', {
            method: 'POST',
            body: formData,
            headers: { 
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken // WAJIB ada agar tidak error 403 Forbidden
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
                // INI KUNCINYA: Refresh halaman agar Django memanggil data terbaru dari PostgreSQL
                location.reload(); 
            } else {
                console.error("Detail Error dari Server:", data.message);
                alert('Gagal Import: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Fetch Error:', error);
            alert('Terjadi kesalahan koneksi ke server. Pastikan server Django jalan.');
        });
    };
});