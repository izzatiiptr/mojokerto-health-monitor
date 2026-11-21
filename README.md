# Mojokerto Health Monitor

**Dashboard Informasi dan Analisis Kesehatan Kota Mojokerto** — proyek akademik Business Intelligence berbasis **Streamlit**.

Menampilkan statistik sumber daya pelayanan kesehatan **2020–2025**, indeks distribusi **HHI dan Gini**, direktori fasilitas kesehatan (setelah verifikasi lokasi), serta estimasi kualitas udara dari **Open-Meteo**.

## Menjalankan aplikasi

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Struktur data

- `data/historis/` — 7 dataset hasil preprocessing Project 1.
- `data/analisis/` — 16 CSV hasil perhitungan dan evaluasi Project 1.
- `data/direktori/fasilitas.csv` — template direktori; koordinat belum diisi sebelum verifikasi.
- `docs/sumber_data.md` — asal data, batasan, dan catatan rekonsiliasi.

Data statis dibaca dari repository; **AQI diambil melalui API**. Visual memakai konsep **Vibrant Healthcare 2.5D** (tosca, navy, coral, amber).

**Status:** kerangka aplikasi awal; bukan situs resmi Pemerintah Kota Mojokerto. Lihat `docs/rencana_pengembangan.md` untuk pekerjaan lanjutan.
