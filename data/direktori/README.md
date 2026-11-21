# Direktori fasilitas pelayanan kesehatan

`fasilitas.csv` berisi kolom:

`Nama_Fasilitas, Jenis_Fasilitas, Kecamatan, Alamat, Latitude, Longitude, Google_Maps_URL, Sumber_Verifikasi`

Mulai dari **6 puskesmas dan 6 rumah sakit** yang telah menjadi ruang lingkup direktori awal.
Untuk setiap baris, periksa nama resmi, alamat terkini, kecamatan administratif,
koordinat tepat di pintu masuk/lokasi fasilitas, dan sumber verifikasi.

**Jangan membuat koordinat perkiraan.** Belum adanya titik yang divalidasi berarti
peta menampilkan peta dasar tanpa marker. Tombol petunjuk arah dibuat dari
koordinat yang sudah dimasukkan dan diperiksa, membuka Google Maps di perangkat pengguna.

CSV ini adalah direktori lokasi terkini. Angka 6 RS/6 puskesmas pada Project 1
berasal dari statistik historis dan tidak otomatis dapat dipakai sebagai koordinat fasilitas.
