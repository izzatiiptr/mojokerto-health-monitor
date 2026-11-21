import plotly.express as px
import streamlit as st
from src.data import load_health_data, annual_trend, total_year
from src.config import TEAL, MUTED_TEAL, CORAL, PEACH, PALETTE, KECAMATAN
from src.visuals import hero, kpi, fmt, section, show_chart, note

hero('Fasilitas & Kapasitas',
     'Tren puskesmas, rumah sakit, posyandu, dan kapasitas tempat tidur rumah sakit.',
     'FASILITAS KESEHATAN • 2020–2025')

data = load_health_data()
f1, f2 = st.columns([1, 1])
with f1: tahun = st.select_slider('Tahun', options=list(range(2020, 2026)), value=2025)
with f2: kecamatan = st.selectbox('Wilayah', ['Seluruh Kota'] + KECAMATAN)

labels = [
    ('Puskesmas', TEAL, 'unit'),
    ('Rumah Sakit', CORAL, 'unit'),
    ('Posyandu', MUTED_TEAL, 'unit'),
    ('Tempat Tidur Rumah Sakit', PEACH, 'tempat tidur'),
]
for col, (label, color, unit) in zip(st.columns(4), labels):
    with col:
        kpi(label, fmt(total_year(data, label, tahun, kecamatan)),
            f'{unit} • {tahun}' if (tahun >= 2022 or label != 'Tempat Tidur Rumah Sakit') else 'Data belum tersedia', color)

st.write('')
t1, t2, t3 = st.tabs(['🏥 Fasilitas', '📑 Profil Rumah Sakit', '🛏️ Kapasitas Tempat Tidur'])
with t1:
    left, right = st.columns([1.3, 1], gap='large')
    with left:
        with st.container(border=True):
            section('Tren Jumlah Fasilitas')
            fasilitas = st.selectbox('Pilih jenis fasilitas', ['Puskesmas', 'Rumah Sakit', 'Posyandu'], key='fasilitas_filter')
            trend = annual_trend(data, fasilitas, kecamatan)
            fig = px.line(trend, x='Tahun', y='Jumlah', markers=True, color_discrete_sequence=[TEAL])
            fig.update_xaxes(dtick=1)
            show_chart(fig)
    with right:
        with st.container(border=True):
            section('Fasilitas per Kecamatan')
            raw = data[fasilitas]
            filtered = raw[raw['Tahun'] == tahun]
            if kecamatan != 'Seluruh Kota':
                filtered = filtered[filtered['Kecamatan'] == kecamatan]
            by_kec = filtered.groupby('Kecamatan', as_index=False)['Jumlah'].sum()
            fig = px.bar(by_kec, x='Kecamatan', y='Jumlah', color='Kecamatan', color_discrete_sequence=PALETTE)
            show_chart(fig)
    st.caption('Data puskesmas 2023 menggunakan hasil rekonsiliasi Project 1, bukan nilai nol pada sumber awal.')

with t2:
    jenis_pilihan = {
        'Jenis Rumah Sakit': ('Rumah Sakit', 'Jenis Rumah Sakit'),
        'Kelas Rumah Sakit': ('Rumah Sakit Berdasarkan Kelas', 'Kelas Rumah Sakit'),
        'Akreditasi Rumah Sakit': ('Rumah Sakit Berdasarkan Akreditasi', 'Akreditasi Rumah Sakit'),
    }
    kategori = st.radio('Klasifikasi', list(jenis_pilihan), horizontal=True)
    label, kolom = jenis_pilihan[kategori]
    raw = data[label]
    raw = raw[raw['Tahun'] == tahun]
    if kecamatan != 'Seluruh Kota':
        raw = raw[raw['Kecamatan'] == kecamatan]
    grouped = raw.groupby(kolom, as_index=False)['Jumlah'].sum().sort_values('Jumlah', ascending=False)
    with st.container(border=True):
        section(f'Komposisi Berdasarkan {kategori} • {tahun}')
        fig = px.bar(grouped, x=kolom, y='Jumlah', color=kolom, color_discrete_sequence=PALETTE)
        show_chart(fig)
        st.dataframe(grouped, hide_index=True, use_container_width=True)
    note('Data jenis, kelas, dan akreditasi mengelompokkan rumah sakit yang sama. Jumlahnya tidak boleh dijumlahkan antar-klasifikasi.')

with t3:
    if tahun < 2022:
        st.warning('Data jumlah tempat tidur tahun 2020–2021 tidak tersedia sebagai pengamatan valid. Pilih tahun 2022–2025.')
    with st.container(border=True):
        section('Perubahan Kapasitas Tempat Tidur • 2022–2025')
        trend = annual_trend(data, 'Tempat Tidur Rumah Sakit', kecamatan)
        fig = px.line(trend, x='Tahun', y='Jumlah', markers=True, color_discrete_sequence=[CORAL])
        fig.update_xaxes(dtick=1)
        show_chart(fig)
    if tahun >= 2022:
        raw = data['Tempat Tidur Rumah Sakit']
        raw = raw[raw['Tahun'] == tahun]
        if kecamatan != 'Seluruh Kota':
            raw = raw[raw['Kecamatan'] == kecamatan]
        by_class = raw.groupby('Kelas Rumah Sakit', as_index=False)['Jumlah'].sum().sort_values('Jumlah')
        with st.container(border=True):
            section(f'Kapasitas Menurut Kelas Tempat Tidur • {tahun}')
            fig = px.bar(by_class, x='Jumlah', y='Kelas Rumah Sakit', orientation='h', color_discrete_sequence=[MUTED_TEAL])
            show_chart(fig)
            st.dataframe(by_class, hide_index=True, use_container_width=True)
    st.caption('Kapasitas tempat tidur adalah jumlah unit tersedia; bukan okupansi atau tingkat keterisian.')
