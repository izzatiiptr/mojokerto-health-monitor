# Status dan pengembangan

## Sudah diimplementasikan (versi prototipe 0.2)

- Navigasi lima halaman dengan Streamlit.
- Palet Teal & Peach dan *soft 2.5D floating shadow*.
- Pintasan merah `#D62828` ke `tel:112`.
- Beranda berisi KPI dan widget AQI, pemanggilan API dengan cache 30 menit; tidak ada menu AQI terpisah.
- Grafik tren dan komposisi tenaga kesehatan, fasilitas dan kapasitas.
- Perhitungan HHI/Gini dibaca dari CSV hasil Project 1.
- Peta interaktif selalu ditampilkan, marker dibuat dari koordinat yang sudah diisi pada CSV direktori.

## Belum selesai / harus diverifikasi

1. **Direktori:** kumpulkan nama, alamat, kecamatan, koordinat peta presisi, tautan Google Maps, dan sumber tiap fasilitas. Periksa silang dengan sumber resmi dan uji tautan navigasinya. Saat ini template masih kosong.
2. **Uji aplikasi:** jalankan Streamlit melalui browser desktop & ponsel; uji semua filter, popup, responsivitas, dan aksesibilitas.
3. **API AQI:** uji permintaan jaringan pada lokasi deployment dan perilaku fallback bila API gagal; kategori adalah US AQI.
4. **Berkas pendukung:** lengkapi bukti sumber dan rekonsiliasi puskesmas 2023 sebelum publikasi.
5. **Deploy:** commit file ke repo GitHub pengguna dan deploy Streamlit Community Cloud.

Pengisian CSV direktori bukan tahap *data mining* atau pemodelan machine learning; ini adalah **pengumpulan dan verifikasi data geospasial**.
