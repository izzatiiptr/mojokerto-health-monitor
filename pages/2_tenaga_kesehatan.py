import plotly.express as px
import streamlit as st
from src.config import TEAL, CORAL, MUTED_TEAL, PALETTE, KECAMATAN
from src.data import load_health_data
from src.visuals import hero, kpi, fmt, show_chart, section, note

hero('Tenaga Kesehatan',
     'Eksplorasi jumlah, jenis profesi, dan perubahan tenaga kesehatan antar-kecamatan.',
     'ANALISIS SUMBER DAYA • 2020–2025')

df = load_health_data()['Tenaga Kesehatan']
jenis_all = sorted(df['Tenaga Kesehatan'].dropna().unique().tolist())
f1, f2, f3 = st.columns([1.2, 1, 1])
with f1:
    profesi = st.selectbox('Jenis tenaga kesehatan', ['Semua jenis'] + jenis_all)
with f2:
    kecamatan = st.selectbox('Wilayah', ['Seluruh Kota'] + KECAMATAN)
with f3:
    tahun = st.select_slider('Tahun detail', options=list(range(2020, 2026)), value=2025)

trend_df = df[df['Semester'] == 2].copy()  # stok akhir tahun; jangan jumlah dua semester
if profesi != 'Semua jenis':
    trend_df = trend_df[trend_df['Tenaga Kesehatan'] == profesi]
if kecamatan != 'Seluruh Kota':
    trend_df = trend_df[trend_df['Kecamatan'] == kecamatan]

by_year = trend_df.groupby('Tahun', as_index=False)['Jumlah'].sum().sort_values('Tahun')
cur = int(by_year.loc[by_year['Tahun'] == tahun, 'Jumlah'].sum())
prev = by_year.loc[by_year['Tahun'] == tahun - 1, 'Jumlah']
delta = cur - int(prev.iloc[0]) if len(prev) else None

c1, c2, c3 = st.columns(3)
with c1: kpi('Jumlah terpilih', fmt(cur), f'Semester II • {tahun}', TEAL)
with c2: kpi('Perubahan dari tahun sebelumnya', f"{delta:+,}".replace(',', '.') if delta is not None else '—', 'orang' if profesi == 'Semua jenis' else 'jumlah', CORAL)
with c3: kpi('Cakupan data', '2020–2025', 'Sumber: hasil pengolahan Project 1', MUTED_TEAL)

left, right = st.columns([1.4, 1], gap='large')
with left:
    with st.container(border=True):
        section('Tren Tahunan')
        fig = px.line(by_year, x='Tahun', y='Jumlah', markers=True, color_discrete_sequence=[TEAL])
        fig.update_xaxes(dtick=1)
        show_chart(fig)
with right:
    with st.container(border=True):
        section('Perbandingan Kecamatan')
        area = df[(df['Semester'] == 2) & (df['Tahun'] == tahun)]
        if profesi != 'Semua jenis':
            area = area[area['Tenaga Kesehatan'] == profesi]
        if kecamatan != 'Seluruh Kota':
            area = area[area['Kecamatan'] == kecamatan]
        summary_area = area.groupby('Kecamatan', as_index=False)['Jumlah'].sum()
        fig = px.bar(summary_area, x='Kecamatan', y='Jumlah', color='Kecamatan',
                     color_discrete_sequence=PALETTE)
        show_chart(fig)

with st.container(border=True):
    section('Komposisi Tenaga Kesehatan')
    jenis_df = trend_df[trend_df['Tahun'] == tahun].groupby('Tenaga Kesehatan', as_index=False)['Jumlah'].sum()
    jenis_df = jenis_df.sort_values('Jumlah')
    fig = px.bar(jenis_df, x='Jumlah', y='Tenaga Kesehatan', orientation='h', color_discrete_sequence=[MUTED_TEAL])
    show_chart(fig, height=max(350, len(jenis_df) * 30))
    with st.expander('Lihat tabel komposisi'):
        st.dataframe(jenis_df.sort_values('Jumlah', ascending=False), hide_index=True, use_container_width=True)

note('Perbandingan tahunan menggunakan Semester II untuk mencegah penghitungan ganda stok tenaga kesehatan. Data ini belum dinormalisasi berdasarkan jumlah penduduk.')
