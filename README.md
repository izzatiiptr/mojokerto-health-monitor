# Mojokerto Health Monitor

**Dashboard Informasi dan Analisis Kesehatan Kota Mojokerto.** Proyek akademik mata kuliah Kecerdasan Bisnis, dikembangkan dengan **Python + Streamlit** menggunakan data Project 1 (2020–2025).

## Fitur

- **Beranda:** lima KPI 2025, tren ringkas, dan widget estimasi **US AQI** Open-Meteo beserta PM2.5/PM10.
- **Tenaga Kesehatan:** eksplorasi tren, komposisi profesi, perbandingan kecamatan, dan pemilihan rentang tahun awal–akhir.
- **Fasilitas & Kapasitas:** puskesmas, rumah sakit, posyandu, tempat tidur RS (mulai 2022), dan filter rentang tahun.
- **Analisis Distribusi:** indeks HHI dan Gini antar tiga kecamatan, beserta tren sesuai rentang tahun.
- **Peta & Direktori:** peta dasar **OpenStreetMap** dapat ditampilkan meskipun CSV direktori masih kosong. 12 entri direktori sudah tampil dan tautan Google Maps/petunjuk arah tersedia tanpa koordinat. **Marker hanya tampil setelah koordinat lokasi diverifikasi**.
- **Darurat 112:** pintasan `tel:112` di sidebar, bukan panggilan otomatis.

## Menjalankan

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

**Deploy:** unggah seluruh isi proyek ke GitHub, lalu atur Streamlit Community Cloud dengan file utama `app.py`.

## Struktur data

- `data/historis/`: 7 CSV hasil preprocessing Project 1, dibaca langsung dari repository.
- `data/analisis/`: 16 CSV hasil perhitungan Project 1.
- `data/direktori/fasilitas.csv`: 12 entri fasilitas dengan alamat dan tautan Google Maps; koordinat masih kosong hingga verifikasi pin.
- `docs/sumber_data.md`: catatan sumber, rekonsiliasi data, dan batasan.

**Desain:** Teal & Peach, *soft 2.5D shadow*. Red darurat **`#D62828`**.

**Batasan:** jumlah tenaga kesehatan tahunan memakai Semester II; tempat tidur 2020–2021 tidak dianalisis; data puskesmas 2023 direkonsiliasi. Nilai AQI adalah estimasi model Open-Meteo, **bukan** ISPU Indonesia maupun pembacaan sensor lokal. Dashboard ini **bukan situs resmi pemerintah**.
