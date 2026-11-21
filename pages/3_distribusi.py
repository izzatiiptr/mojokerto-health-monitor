import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.data import load_health_data, load_distribution_index, annual, annual_trend
from src.config import TEAL, CORAL, AMBER, NAVY, PALETTE
from src.visuals import hero, kpi, note, fmt, show_chart

hero('Distribusi & Kapasitas Pelayanan Kesehatan',
     'Perbandingan sumber daya antar-kecamatan, konsentrasi HHI, dan ketimpangan Gini.',
     'ANALISIS STATISTIK')
data = load_health_data()
indeks = load_distribution_index()
labels = ['Tenaga Kesehatan','Puskesmas','Rumah Sakit Berdasarkan Jenis','Posyandu',
          'Tempat Tidur Rumah Sakit']
indikator = st.selectbox('Indikator',labels)
awal = 2022 if indikator == 'Tempat Tidur Rumah Sakit' else 2020
tahun = st.slider('Tahun',min_value=awal,max_value=2025,value=2025)
key = 'Rumah Sakit' if indikator == 'Rumah Sakit Berdasarkan Jenis' else indikator
raw = annual(data[key],tenaga=key=='Tenaga Kesehatan')
by_kec = raw[raw['Tahun']==tahun].groupby('Kecamatan',as_index=False)['Jumlah'].sum()
entry = indeks[(indeks['Indikator']==indikator)&(indeks['Tahun']==tahun)]
if entry.empty:
    st.warning('Nilai indeks belum tersedia untuk pilihan ini.')
else:
    cols = st.columns(3)
    with cols[0]: kpi('Total',fmt(by_kec['Jumlah'].sum()),f'{indikator} • {tahun}',TEAL)
    with cols[1]: kpi('HHI',f"{entry['HHI'].iloc[0]:.4f}",'Konsentrasi antar-kecamatan',CORAL)
    with cols[2]: kpi('Gini',f"{entry['Gini'].iloc[0]:.4f}",'Ketimpangan jumlah antar-kecamatan',AMBER)
st.subheader('Distribusi per kecamatan')
show_chart(px.bar(by_kec,x='Kecamatan',y='Jumlah',color='Kecamatan',color_discrete_sequence=PALETTE))
st.subheader('Perkembangan indeks')
idx = indeks[indeks['Indikator']==indikator].sort_values('Tahun')
fig = go.Figure()
fig.add_scatter(x=idx['Tahun'],y=idx['HHI'],mode='lines+markers',name='HHI',line=dict(color=TEAL,width=3))
fig.add_scatter(x=idx['Tahun'],y=idx['Gini'],mode='lines+markers',name='Gini',line=dict(color=CORAL,width=3))
show_chart(fig)
note('Untuk tiga kecamatan, HHI berkisar 1/3–1 dan Gini 0–2/3. Indeks memakai jumlah absolut, bukan jumlah per penduduk.')
st.subheader('Kapasitas tempat tidur RS')
kapasitas = annual_trend(data,'Tempat Tidur Rumah Sakit')
show_chart(px.line(kapasitas,x='Tahun',y='Jumlah',markers=True,color_discrete_sequence=[NAVY]))
st.caption('Jumlah tempat tidur ditampilkan mulai 2022. Angka 2020–2021 pada data kerja bukan pengamatan valid.')
