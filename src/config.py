"""Konfigurasi warna, lokasi file, dan cakupan data."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_HISTORIS = ROOT / 'data' / 'historis'
DATA_ANALISIS = ROOT / 'data' / 'analisis'
DATA_DIREKTORI = ROOT / 'data' / 'direktori' / 'fasilitas.csv'

# Teal & Peach — palet visual pilihan pengguna.
TEAL = '#0F6B6D'
MUTED_TEAL = '#5FA8A0'
CREAM = '#FFF4E8'
PEACH = '#F7B08A'
CORAL = '#E76E51'
DARK = '#203537'
RED_112 = '#D62828'  # Hanya untuk aksi darurat; hindari memakai sebagai warna grafik.
PALETTE = [TEAL, CORAL, MUTED_TEAL, PEACH, '#597D8A', '#A7857C']
KECAMATAN = ['Kranggan', 'Magersari', 'Prajuritkulon']

LABEL_FILES = {
    'Tenaga Kesehatan': 'tenaga_kesehatan.csv',
    'Puskesmas': 'puskesmas.csv',
    'Rumah Sakit': 'rumah_sakit_berdasarkan_jenis.csv',
    'Posyandu': 'posyandu.csv',
    'Tempat Tidur Rumah Sakit': 'tempat_tidur_rumah_sakit.csv',
    'Rumah Sakit Berdasarkan Kelas': 'rumah_sakit_berdasarkan_kelas.csv',
    'Rumah Sakit Berdasarkan Akreditasi': 'rumah_sakit_berdasarkan_akreditasi.csv',
}
# Perkiraan titik tengah Kota Mojokerto, dipakai untuk permintaan API dan pusat peta.
# BUKAN koordinat fasilitas kesehatan.
AQI_LAT, AQI_LON = -7.472, 112.434
