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
