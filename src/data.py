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

@st.cache_data(show_spinner=False)
def load_directory():
    df = pd.read_csv(DATA_DIREKTORI)
    for col in ['Nama_Fasilitas','Jenis_Fasilitas','Kecamatan','Alamat','Google_Maps_URL','Sumber_Verifikasi']:
        df[col] = df[col].fillna('').astype(str).str.strip()
    for col in ['Latitude','Longitude']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
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
