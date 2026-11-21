"""Validasi dasar dataset; jalankan: python tests/validasi_data.py."""
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parents[1]
hist = root / 'data' / 'historis'
analysis = root / 'data' / 'analisis'

files = {
    'Tenaga Kesehatan': 'tenaga_kesehatan.csv',
    'Puskesmas': 'puskesmas.csv',
    'Rumah Sakit': 'rumah_sakit_berdasarkan_jenis.csv',
    'Posyandu': 'posyandu.csv',
    'Tempat Tidur Rumah Sakit': 'tempat_tidur_rumah_sakit.csv'
}
expect = {
    'Tenaga Kesehatan': 2257, 'Puskesmas': 6,
    'Rumah Sakit': 6, 'Posyandu': 176, 'Tempat Tidur Rumah Sakit': 781
}
for label, filename in files.items():
    df = pd.read_csv(hist / filename)
    assert {'Tahun','Jumlah','Kecamatan'}.issubset(df.columns), filename
    df = df[df['Tahun']==2025]
    if label == 'Tenaga Kesehatan':
        df = df[df['Semester']==2]
    n = int(df['Jumlah'].sum())
    assert n == expect[label], f'{label}: {n} bukan {expect[label]}'
    print(f'{label} (2025): {n} — OK')

puskesmas = pd.read_csv(hist / 'puskesmas.csv')
assert puskesmas[puskesmas['Tahun']==2023]['Jumlah'].sum()==6
indeks = pd.read_csv(analysis / 'indeks_distribusi.csv')
assert {'Indikator','Tahun','HHI','Gini'}.issubset(indeks.columns)
assert indeks[(indeks['Indikator']=='Tempat Tidur Rumah Sakit') & (indeks['Tahun']<2022)].empty
assert len(list(hist.glob('*.csv'))) == 7
assert len(list(analysis.glob('*.csv'))) == 16
print('Seluruh pemeriksaan dataset awal: OK')

# Uji ulang HHI dan Gini terhadap tabel historis yang tampil di dashboard.
file_for_index = {
    'Tenaga Kesehatan': 'tenaga_kesehatan.csv',
    'Puskesmas': 'puskesmas.csv',
    'Posyandu': 'posyandu.csv',
    'Rumah Sakit Berdasarkan Jenis': 'rumah_sakit_berdasarkan_jenis.csv',
    'Rumah Sakit Berdasarkan Kelas': 'rumah_sakit_berdasarkan_kelas.csv',
    'Rumah Sakit Berdasarkan Akreditasi': 'rumah_sakit_berdasarkan_akreditasi.csv',
    'Tempat Tidur Rumah Sakit': 'tempat_tidur_rumah_sakit.csv',
}
for _, row in indeks.iterrows():
    d = pd.read_csv(hist / file_for_index[row['Indikator']])
    d = d[d['Tahun'] == row['Tahun']]
    if row['Indikator'] == 'Tenaga Kesehatan':
        d = d[d['Semester'] == 2]
    counts = d.groupby('Kecamatan')['Jumlah'].sum().tolist()
    assert len(counts) == 3 and sum(counts) > 0, row.to_dict()
    total = sum(counts)
    hhi = sum((x / total) ** 2 for x in counts)
    gini = sum(abs(x - y) for x in counts for y in counts) / (2 * len(counts) * total)
    assert abs(hhi - row['HHI']) < 1e-6, f"HHI {row['Indikator']} {row['Tahun']}"
    assert abs(gini - row['Gini']) < 1e-6, f"Gini {row['Indikator']} {row['Tahun']}"
print(f'Uji ulang indeks distribusi: {len(indeks)} baris — OK')

required_pages = [
    '1_beranda.py', '2_tenaga_kesehatan.py', '3_fasilitas_kapasitas.py',
    '4_distribusi.py', '5_direktori.py',
]
assert sorted(p.name for p in (root / 'pages').glob('*.py')) == required_pages
assert '#D62828' in (root / 'assets' / 'styles.css').read_text(encoding='utf-8')
assert 'tel:112' in (root / 'app.py').read_text(encoding='utf-8')
print('Navigasi dan tombol 112: OK')

# Pemeriksaan statis perubahan antarmuka v0.3.
app = (root / 'app.py').read_text(encoding='utf-8')
page_map = (root / 'pages' / '5_direktori.py').read_text(encoding='utf-8')
page_dist = (root / 'pages' / '4_distribusi.py').read_text(encoding='utf-8')
assert "position='hidden'" in app
assert 'st.page_link(page' in app
assert "tiles='OpenStreetMap'" in page_map
assert "tiles='CartoDB positron'" not in page_map
for page in ('2_tenaga_kesehatan.py','3_fasilitas_kapasitas.py','4_distribusi.py'):
    source = (root / 'pages' / page).read_text(encoding='utf-8')
    assert 'start_year, end_year = st.slider(' in source, page
assert "'**Gini** mengukur" in page_dist
print('Perubahan v0.3: sidebar, rentang tahun, Markdown, dan basemap — OK')


# Pemeriksaan direktori Google Maps versi v0.4.
from urllib.parse import parse_qs, urlparse
directory = pd.read_csv(root / 'data' / 'direktori' / 'fasilitas.csv')
assert len(directory) == 12
assert set(directory['Jenis_Fasilitas']) == {'Rumah Sakit', 'Puskesmas'}
assert directory['Jenis_Fasilitas'].value_counts().to_dict() == {'Rumah Sakit': 6, 'Puskesmas': 6}
assert set(directory['Kecamatan']).issubset({'Kranggan', 'Magersari', 'Prajuritkulon'})
assert not directory['Nama_Fasilitas'].duplicated().any()
for _, row in directory.iterrows():
    assert isinstance(row['Alamat'], str) and row['Alamat'].strip()
    parts = urlparse(row['Google_Maps_URL'])
    assert parts.scheme == 'https' and parts.netloc == 'www.google.com'
    assert 'query_place_id' in parse_qs(parts.query), row['Nama_Fasilitas']
assert directory['Latitude'].isna().all() and directory['Longitude'].isna().all(), 'Koordinat tidak boleh diisi tanpa verifikasi pin'
app = (root / 'app.py').read_text(encoding='utf-8')
assert "key='sidebar_primary'" in app
assert "key='sidebar_secondary'" in app
assert app.index("class=\"emergency-link\"") < app.index("key='sidebar_secondary'")
map_code = (root / 'pages' / '5_direktori.py').read_text(encoding='utf-8')
assert 'destination_place_id' in map_code
print('Direktori 12 fasilitas, tautan Google Maps, dan tata letak sidebar v0.4: OK')
