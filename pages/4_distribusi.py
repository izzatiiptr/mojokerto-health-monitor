"""Konsentrasi (HHI) dan ketimpangan jumlah (Gini) antar-kecamatan."""
import plotly.express as px
import streamlit as st
from src.data import load_health_data, load_distribution_index, annual
from src.config import TEAL, CORAL, MUTED_TEAL, PALETTE
from src.visuals import hero, kpi, fmt, show_chart, section, note

hero('Analisis Distribusi Antar-Kecamatan',
     'Pola konsentrasi HHI dan ketimpangan Gini berdasarkan jumlah absolut sumber daya kesehatan.',
     'HASIL ANALISIS PROJECT 1')

data = load_health_data()
idx = load_distribution_index()
options = {
    'Tenaga Kesehatan': 'Tenaga Kesehatan',
    'Puskesmas': 'Puskesmas',
    'Rumah Sakit': 'Rumah Sakit Berdasarkan Jenis',
    'Posyandu': 'Posyandu',
    'Tempat Tidur Rumah Sakit': 'Tempat Tidur Rumah Sakit',
}

pilihan = st.selectbox('Indikator sumber daya', list(options))
first_year = 2022 if pilihan == 'Tempat Tidur Rumah Sakit' else 2020
start_year, end_year = st.slider(
    'Rentang tahun indeks (awal – akhir)', min_value=first_year, max_value=2025,
    value=(first_year, 2025), step=1,
    help='KPI dan distribusi kecamatan menggunakan tahun akhir, grafik tren memakai seluruh rentang.',
)

key = options[pilihan]
entry = idx[(idx['Indikator'] == key) & (idx['Tahun'] == end_year)]
raw = annual(data[pilihan], tenaga=pilihan == 'Tenaga Kesehatan')
by_kec = raw[raw['Tahun'] == end_year].groupby('Kecamatan', as_index=False)['Jumlah'].sum()
idtr = (idx[(idx['Indikator'] == key) & idx['Tahun'].between(start_year, end_year)]
        .sort_values('Tahun'))

st.markdown('<div class="kpi-group-space"></div>', unsafe_allow_html=True)
if entry.empty:
    st.info('Indeks untuk tahun akhir terpilih belum tersedia.')
else:
    record = entry.iloc[0]
    for col, (label, value, desc, color) in zip(st.columns(3, gap='large'), [
        ('Jumlah teramati', fmt(by_kec['Jumlah'].sum()), f'{pilihan} • {end_year}', TEAL),
        ('HHI', f"{record['HHI']:.4f}", 'Konsentrasi proporsi tiga kecamatan', CORAL),
        ('Koefisien Gini', f"{record['Gini']:.4f}", 'Ketimpangan jumlah tiga kecamatan', MUTED_TEAL),
    ]):
        with col:
            kpi(label, value, desc, color)

st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
left, right = st.columns([1.1, 1], gap='large')
with left:
    with st.container(border=True):
        section(f'Distribusi Jumlah • {end_year}')
        fig = px.bar(by_kec, x='Kecamatan', y='Jumlah', color='Kecamatan',
                     color_discrete_sequence=PALETTE)
        show_chart(fig, height=340)
with right:
    with st.container(border=True):
        section(f'Tren HHI • {start_year}–{end_year}')
        fig = px.line(idtr, x='Tahun', y='HHI', markers=True,
                      color_discrete_sequence=[TEAL])
        fig.update_xaxes(dtick=1)
        show_chart(fig, height=340)

st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
with st.container(border=True):
    section(f'Tren Koefisien Gini • {start_year}–{end_year}')
    fig = px.line(idtr, x='Tahun', y='Gini', markers=True,
                  color_discrete_sequence=[CORAL])
    fig.update_xaxes(dtick=1)
    show_chart(fig, height=310)

with st.expander('Apa arti HHI dan Gini?'):
    # Tanpa indentasi pada Markdown multiline: indentasi >= 4 spasi membentuk blok kode
    # sehingga tanda ** muncul mentah dan teks tidak membungkus dengan benar.
    st.markdown(
        '**HHI** mengukur konsentrasi proporsi sumber daya pada tiga kecamatan. '
        'Untuk tiga kecamatan, nilai minimum **1/3** (jumlah sama) dan '
        'maksimum **1** (seluruh sumber daya di satu kecamatan).\n\n'
        '**Gini** mengukur ketimpangan jumlah antar-kecamatan. '
        'Nilai minimum **0** (jumlah sama) dan maksimum **2/3** untuk tiga kecamatan.\n\n'
        'Kedua indeks **tidak** menunjukkan kecukupan fasilitas berdasarkan penduduk, '
        'kebutuhan pelayanan, atau waktu tempuh menuju layanan kesehatan.'
    )

note('Interpretasi kebijakan: indeks adalah alat skrining distribusi, bukan bukti bahwa pelayanan sudah merata atau suatu kecamatan harus menerima fasilitas tambahan. Tinjau populasi, kebutuhan, dan aksesibilitas sebelum mengambil keputusan.')
