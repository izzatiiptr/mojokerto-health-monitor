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
