# Direktori fasilitas kesehatan (pembaruan v0.4)

Dataset `fasilitas.csv` memuat **12 entri**: 6 rumah sakit dan 6 puskesmas Kota Mojokerto.

**Acuan lokasi:** kolom `Alamat` dan `Google_Maps_URL` mengikuti daftar listing Google Maps yang dikumpulkan pada tahap persiapan. Setiap URL memuat `query_place_id` sehingga pengguna dapat membuka listing Google Maps dan tombol **Petunjuk arah**. Verifikasi lapangan/visual terakhir atas pin tetap diperlukan sebelum menyatakan koordinat valid.

**Acuan kecamatan:** kolom `Kecamatan` distandardisasi ke `Kranggan`, `Magersari`, dan `Prajuritkulon` agar konsisten dengan dataset historis dan filter aplikasi. Nama kecamatan pada alamat mengikuti penamaan dalam listing Google Maps, sehingga mungkin berbeda dengan kolom filter administratif.

## Koordinat dan marker

Kolom `Latitude` dan `Longitude` masih kosong: **0 dari 12 fasilitas memiliki koordinat yang diperiksa terhadap pin Google Maps**. Karena itu, halaman menampilkan 12 kartu direktori, tombol Google Maps, dan Petunjuk arah, tetapi **belum menampilkan 12 marker pada peta OpenStreetMap**.

Untuk melengkapi lokasi:

1. Klik `Google_Maps_URL` dan pastikan listing sesuai nama fasilitas.
2. Pada Google Maps desktop, klik kanan tepat pada pin/lokasi bangunan (bukan jalan di dekatnya).
3. Salin pasangan koordinat yang ditampilkan: angka pertama ke `Latitude`, angka kedua ke `Longitude`.
4. Simpan file CSV dengan header dan penamaan yang sama.
5. Setelah commit CSV ke GitHub, marker akan tampil untuk baris yang koordinatnya diisi dan memenuhi validasi batas koordinat Kota Mojokerto.

## Perbedaan alamat yang perlu diperiksa

- Puskesmas Kedundung: listing Google Maps memakai Jl. Totok Kerot; dokumen lama menyebut Jl. Raya Bypass.
- Puskesmas Mentikan: listing Google Maps menyebut No. 55, sementara sebagian dokumen lama menyebut No. 54.
- Puskesmas Gedongan: listing Google Maps menyebut Jl. Sawunggaling; dokumen pemerintah lebih lama ada yang menyebut Jl. Gajah Mada.

**Sumber pendukung:** https://web.mojokertokota.go.id/fasilitas/detail/rumah-sakit-qcpzwakulw dan https://satikomo.mojokertokota.go.id/sdi?page=2. Dataset direktori bukan hasil geocoding otomatis atau lokasi hasil prediksi.
