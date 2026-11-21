"""Eksplorasi stok tenaga kesehatan dengan rentang tahun mulai–akhir."""
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

st.markdown('<div class="filter-heading">Filter eksplorasi</div>', unsafe_allow_html=True)
f1, f2 = st.columns([1.2, 1], gap='large')
with f1:
    profesi = st.selectbox('Jenis tenaga kesehatan', ['Semua jenis'] + jenis_all)
with f2:
    kecamatan = st.selectbox('Wilayah', ['Seluruh Kota'] + KECAMATAN)

start_year, end_year = st.slider(
    'Rentang tahun (awal – akhir)',
    min_value=2020, max_value=2025, value=(2020, 2025), step=1,
    help='Grafik hanya menampilkan rentang ini. KPI jumlah dan komposisi menggunakan tahun akhir.',
)

# Data tenaga kesehatan merupakan stok semesteran; tren tahunan memakai Semester II.
trend_df = df[df['Semester'] == 2].copy()
if profesi != 'Semua jenis':
    trend_df = trend_df[trend_df['Tenaga Kesehatan'] == profesi]
if kecamatan != 'Seluruh Kota':
    trend_df = trend_df[trend_df['Kecamatan'] == kecamatan]

by_year = (trend_df.groupby('Tahun', as_index=False)['Jumlah'].sum()
           .sort_values('Tahun'))
visible_year = by_year[by_year['Tahun'].between(start_year, end_year)].copy()
start_total = int(by_year.loc[by_year['Tahun'] == start_year, 'Jumlah'].sum())
end_total = int(by_year.loc[by_year['Tahun'] == end_year, 'Jumlah'].sum())
delta = end_total - start_total

st.markdown('<div class="kpi-group-space"></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3, gap='large')
with c1:
    kpi('Jumlah pada tahun akhir', fmt(end_total), f'Semester II • {end_year}', TEAL)
with c2:
    kpi('Perubahan selama rentang', f"{delta:+,}".replace(',', '.'),
        f'Selisih {end_year} terhadap {start_year} • orang', CORAL)
with c3:
    kpi('Periode ditampilkan', f'{start_year}–{end_year}',
        'Tahun awal – tahun akhir', MUTED_TEAL)

st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
left, right = st.columns([1.4, 1], gap='large')
with left:
    with st.container(border=True):
        section(f'Tren Tahunan • {start_year}–{end_year}')
        fig = px.line(visible_year, x='Tahun', y='Jumlah', markers=True,
                      color_discrete_sequence=[TEAL])
        fig.update_xaxes(dtick=1)
        show_chart(fig)
with right:
    with st.container(border=True):
        section(f'Perbandingan Kecamatan • {end_year}')
        area = df[(df['Semester'] == 2) & (df['Tahun'] == end_year)]
        if profesi != 'Semua jenis':
            area = area[area['Tenaga Kesehatan'] == profesi]
        if kecamatan != 'Seluruh Kota':
            area = area[area['Kecamatan'] == kecamatan]
        summary_area = area.groupby('Kecamatan', as_index=False)['Jumlah'].sum()
        fig = px.bar(summary_area, x='Kecamatan', y='Jumlah', color='Kecamatan',
                     color_discrete_sequence=PALETTE)
        show_chart(fig)

st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
with st.container(border=True):
    section(f'Komposisi Tenaga Kesehatan • {end_year}')
    jenis_df = (trend_df[trend_df['Tahun'] == end_year]
                .groupby('Tenaga Kesehatan', as_index=False)['Jumlah'].sum()
                .sort_values('Jumlah'))
    fig = px.bar(jenis_df, x='Jumlah', y='Tenaga Kesehatan', orientation='h',
                 color_discrete_sequence=[MUTED_TEAL])
    show_chart(fig, height=max(380, len(jenis_df) * 32))
    with st.expander('Lihat tabel komposisi'):
        st.dataframe(jenis_df.sort_values('Jumlah', ascending=False),
                     hide_index=True, use_container_width=True)

note('KPI akhir dan komposisi menggunakan Semester II pada tahun akhir pilihan. Selisih dihitung antara tahun awal dan akhir; tidak sama dengan perubahan tahunan (year-on-year). Data belum dinormalisasi dengan jumlah penduduk.')
