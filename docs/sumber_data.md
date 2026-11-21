# Sumber dan batasan dataset

- **Sumber historis:** dataset SATA JATIM yang digunakan pada Project 1 (Kota Mojokerto, 2020–2025). Folder `data/historis/` berisi hasil transformasi *wide → long* dari tujuh dataset; bukan file mentah dari portal.
- **Sumber indeks dan ringkasan:** hasil analisis Project 1 pada `data/analisis/`, meliputi HHI, koefisien Gini, perubahan tahunan, komposisi, dan audit konsistensi.
- **Tenaga kesehatan:** untuk perbandingan tahunan digunakan **Semester II**, karena Semester I dan Semester II tidak boleh dijumlahkan menjadi satu stok tahunan.
- **Tempat tidur rumah sakit:** 2020–2021 pada data sumber tidak memiliki pengamatan terisi; walaupun kolom `Jumlah` pada data kerja berupa nol, analisis temporal dan grafik **dimulai dari 2022**.
- **Puskesmas 2023:** data awal sumber mencatat nol di ketiga kecamatan; Project 1 menggunakan **data rekonsiliasi** menjadi total 6 puskesmas (Magersari 3, Prajuritkulon 2, Kranggan 1) berdasarkan verifikasi terpisah. **Jangan mengklaim angka ini sama persis dengan data mentah**. Dokumen sumber pendukung dan bukti koreksi wajib dilampirkan sebelum publikasi final.
- **RS:** data berdasarkan jenis, kelas, dan akreditasi adalah tiga cara mengelompokkan **fasilitas yang sama**; jangan menjumlahkan ketiga tabel.
- **HHI/Gini:** memakai jumlah absolut antar tiga kecamatan. Indeks ini **bukan** ukuran kebutuhan menurut populasi, akses geografis, atau kecukupan layanan.
- **Direktori:** `data/direktori/fasilitas.csv` berupa template. Setiap lokasi harus memiliki nama, alamat, dan titik peta yang diperiksa. Informasi peta terkini tidak otomatis sama dengan agregat historis.
- **AQI:** berasal dari Open-Meteo Air Quality API; menampilkan **US AQI**, bukan ISPU Indonesia, dan merupakan estimasi model.

**Data mentah dan notebook pengolahan tetap disimpan di arsip Project 1**, terpisah dari repository aplikasi; perubahan dari sumber asli harus memiliki dokumentasi verifikasi.
