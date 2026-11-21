from pathlib import Path
import pandas as pd
import streamlit as st
from src.config import DATA_HISTORIS, DATA_ANALISIS, DATA_DIREKTORI, LABEL_FILES

@st.cache_data(show_spinner=False)
def load_health_data():
    data = {}
    for label, filename in LABEL_FILES.items():
        df = pd.read_csv(DATA_HISTORIS / filename)
        df['Tahun'] = pd.to_numeric(df['Tahun'], errors='raise').astype(int)
        df['Jumlah'] = pd.to_numeric(df['Jumlah'], errors='raise').astype(int)
        df['Kecamatan'] = df['Kecamatan'].astype(str).str.replace(r'^Kecamatan\s+', '', regex=True).str.strip()
        data[label] = df
    return data

@st.cache_data(show_spinner=False)
def load_distribution_index():
    return pd.read_csv(DATA_ANALISIS / 'indeks_distribusi.csv')

def load_directory():
    """Membaca CSV direktori dengan validasi skema (tidak memakai cache)."""
    path = DATA_DIREKTORI
    if not path.is_file():
        raise FileNotFoundError(
            f"File direktori tidak ditemukan: {path}. "
            "Pastikan data/direktori/fasilitas.csv sudah diunggah pada branch deployment."
        )

    required = [
        'Nama_Fasilitas', 'Jenis_Fasilitas', 'Kecamatan', 'Alamat',
        'Latitude', 'Longitude', 'Google_Maps_URL', 'Sumber_Verifikasi',
    ]

    # CSV unggahan bisa memakai koma atau titik koma, dengan/tanpa BOM.
    # Baca baris header saja untuk memilih separator secara konsisten.
    with path.open('r', encoding='utf-8-sig') as file:
        header = file.readline().strip()
    if not header:
        raise ValueError(f"File direktori kosong tanpa header: {path}")
    sep = ';' if header.count(';') > header.count(',') else ','

    try:
        df = pd.read_csv(path, encoding='utf-8-sig', sep=sep)
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise ValueError(f"CSV direktori tidak bisa dibaca: {exc}") from exc

    # Hilangkan spasi dan karakter BOM yang kadang tersisa pada nama kolom.
    df.columns = df.columns.astype(str).str.replace('\ufeff', '', regex=False).str.strip()
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            f"Kolom fasilitas.csv tidak sesuai. Tidak ditemukan: {missing}. "
            f"Kolom yang terbaca: {list(df.columns)}. "
            "Periksa baris pertama CSV; gunakan template 8 kolom dari paket perbaikan."
        )

    # Pertahankan hanya kolom skema yang dibutuhkan, dengan urutan stabil.
    df = df[required].copy()
    text_cols = [
        'Nama_Fasilitas', 'Jenis_Fasilitas', 'Kecamatan', 'Alamat',
        'Google_Maps_URL', 'Sumber_Verifikasi',
    ]
    for col in text_cols:
        df[col] = df[col].fillna('').astype(str).str.strip()
    for col in ['Latitude', 'Longitude']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    kec_key = (df['Kecamatan']
               .str.replace(r'(?i)^Kecamatan\s+', '', regex=True)
               .str.replace(r'\s+', '', regex=True)
               .str.casefold())
    kec_map = {
        'prajuritkulon': 'Prajuritkulon',
        'kranggan': 'Kranggan',
        'magersari': 'Magersari',
    }
    df['Kecamatan'] = kec_key.map(kec_map).fillna(df['Kecamatan'])

    jenis_key = df['Jenis_Fasilitas'].str.casefold()
    jenis_map = {'rumah sakit': 'Rumah Sakit', 'puskesmas': 'Puskesmas'}
    df['Jenis_Fasilitas'] = jenis_key.map(jenis_map).fillna(df['Jenis_Fasilitas'])
    return df

def annual(df, tenaga=False):
    # Tenaga kesehatan adalah data stok semester; gunakan Semester II untuk total tahunan.
    if tenaga:
        return df[df['Semester'] == 2]
    return df

def annual_trend(data, label, kecamatan='Seluruh Kota'):
    df = annual(data[label], tenaga=label=='Tenaga Kesehatan')
    if label == 'Tempat Tidur Rumah Sakit':
        df = df[df['Tahun'] >= 2022]  # 2020–2021 bukan observasi valid.
    if kecamatan != 'Seluruh Kota':
        df = df[df['Kecamatan'] == kecamatan]
    return df.groupby('Tahun', as_index=False)['Jumlah'].sum()

def total_year(data, label, tahun, kecamatan='Seluruh Kota'):
    df = annual(data[label], tenaga=label=='Tenaga Kesehatan')
    if label == 'Tempat Tidur Rumah Sakit' and tahun < 2022:
        return None
    df = df[df['Tahun'] == tahun]
    if kecamatan != 'Seluruh Kota':
        df = df[df['Kecamatan'] == kecamatan]
    return int(df['Jumlah'].sum())
