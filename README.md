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

## Pembaruan v0.3

- Identitas aplikasi dipindahkan ke atas menu sidebar (navigasi kustom).
- Hero mendapat ruang atas; kartu dan konten analisis dibuat lebih renggang.
- Filter **rentang tahun (awal–akhir)** diterapkan pada halaman analisis, dengan KPI merujuk tahun akhir.
- Penjelasan HHI dan Gini diperbaiki agar Markdown tidak tampil sebagai blok kode.
- Peta dasar beralih dari CartoDB Positron ke OpenStreetMap karena tile sebelumnya menampilkan permintaan API key.

**Status pengujian:** validasi CSV, sintaks, dan eksekusi dengan simulasi widget dilakukan. Tampilan Streamlit dan tile peta pada browser pengguna tetap perlu diverifikasi setelah commit dan redeploy.

## Pembaruan v0.4

- Sidebar dibuat ringkas: judul, lima menu, dan tombol **112 merah** berada dalam area primer sebelum bagian informasi data yang dapat digulir. Pada layar yang pendek, scroll mungkin tetap diperlukan.
- `data/direktori/fasilitas.csv` berisi 12 entri alamat dan listing Google Maps, serta ejaan kecamatan yang konsisten dengan data historis.
- Daftar fasilitas dan tombol **Google Maps / Petunjuk arah** tersedia walaupun koordinat pin belum diisi.
- Peta dasarnya tetap OpenStreetMap; marker hanya tampil untuk koordinat yang sudah diverifikasi terhadap pin Google Maps.
