import plotly.express as px
import plotly.graph_objects as go
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
f1, f2 = st.columns([1.5, 1])
with f1:
    pilihan = st.selectbox('Indikator', list(options))
with f2:
    start = 2022 if pilihan == 'Tempat Tidur Rumah Sakit' else 2020
    tahun = st.select_slider('Tahun', options=list(range(start, 2026)), value=2025)

key = options[pilihan]
entry = idx[(idx['Indikator'] == key) & (idx['Tahun'] == tahun)]
raw = annual(data[pilihan], tenaga=pilihan == 'Tenaga Kesehatan')
by_kec = raw[raw['Tahun'] == tahun].groupby('Kecamatan', as_index=False)['Jumlah'].sum()
if entry.empty:
    st.info('Indeks untuk tahun terpilih belum tersedia.')
else:
    record = entry.iloc[0]
    for col, (label, value, desc, color) in zip(st.columns(3), [
        ('Jumlah teramati', fmt(by_kec['Jumlah'].sum()), f'{pilihan} • {tahun}', TEAL),
        ('HHI', f"{record['HHI']:.4f}", 'Konsentrasi proporsi tiga kecamatan', CORAL),
        ('Koefisien Gini', f"{record['Gini']:.4f}", 'Ketimpangan jumlah tiga kecamatan', MUTED_TEAL),
    ]):
        with col: kpi(label, value, desc, color)

left, right = st.columns([1.1, 1], gap='large')
with left:
    with st.container(border=True):
        section(f'Distribusi Jumlah • {tahun}')
        fig = px.bar(by_kec, x='Kecamatan', y='Jumlah', color='Kecamatan',
                     color_discrete_sequence=PALETTE)
        show_chart(fig, height=340)
with right:
    with st.container(border=True):
        section('Tren HHI')
        idtr = idx[idx['Indikator'] == key].sort_values('Tahun')
        fig = px.line(idtr, x='Tahun', y='HHI', markers=True, color_discrete_sequence=[TEAL])
        fig.update_xaxes(dtick=1)
        show_chart(fig, height=340)

with st.container(border=True):
    section('Tren Koefisien Gini')
    fig = px.line(idtr, x='Tahun', y='Gini', markers=True, color_discrete_sequence=[CORAL])
    fig.update_xaxes(dtick=1)
    show_chart(fig, height=310)

with st.expander('Apa arti HHI dan Gini?'):
    st.markdown('''**HHI** mengukur konsentrasi bagian sumber daya pada tiga kecamatan. Untuk tiga kecamatan,
    nilai minimumnya **1/3** (jumlah sama) dan nilai maksimumnya **1** (semuanya di satu kecamatan).

    **Gini** mengukur ketimpangan jumlah antar-kecamatan. Nilai minimalnya **0** (jumlah sama),
    dan nilai maksimal pada tiga kecamatan adalah **2/3**.

    Kedua indeks **tidak** menunjukkan kecukupan fasilitas berdasarkan penduduk, kebutuhan pelayanan,
    maupun waktu tempuh menuju layanan kesehatan.''')

note('Interpretasi kebijakan: indeks adalah alat skrining distribusi, bukan bukti bahwa pelayanan sudah merata atau suatu kecamatan harus menerima fasilitas tambahan. Tinjau populasi, kebutuhan, dan aksesibilitas sebelum mengambil keputusan.')
