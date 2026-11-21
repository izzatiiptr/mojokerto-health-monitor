from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_HISTORIS = ROOT / 'data' / 'historis'
DATA_ANALISIS = ROOT / 'data' / 'analisis'
DATA_DIREKTORI = ROOT / 'data' / 'direktori' / 'fasilitas.csv'

TEAL = '#00B8A9'
NAVY = '#12304A'
CORAL = '#FF6B57'
AMBER = '#FFBE3D'
PALETTE = [TEAL, NAVY, CORAL, AMBER, '#3E83D5', '#785CC5']
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

# Koordinat pusat pendekatan hanya digunakan untuk API kualitas udara;
# BUKAN lokasi sebuah rumah sakit atau puskesmas.
AQI_LAT, AQI_LON = -7.472, 112.434
