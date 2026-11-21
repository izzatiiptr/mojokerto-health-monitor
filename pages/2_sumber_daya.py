import streamlit as st
import plotly.express as px
from src.data import load_health_data, annual, annual_trend, total_year
from src.config import TEAL, CORAL, KECAMATAN
from src.visuals import hero, kpi, fmt, show_chart

hero('Sumber Daya Pelayanan Kesehatan',
     'Eksplorasi jumlah dan perubahan sumber daya berdasarkan indikator, tahun, dan kecamatan.',
     'ANALISIS HISTORIS • 2020–2025')
data = load_health_data()
c1,c2,c3 = st.columns(3)
with c1:
    indikator = st.selectbox('Indikator', ['Tenaga Kesehatan','Puskesmas','Rumah Sakit','Posyandu',
                                      'Tempat Tidur Rumah Sakit','Rumah Sakit Berdasarkan Kelas',
                                      'Rumah Sakit Berdasarkan Akreditasi'])
with c2:
    kecamatan = st.selectbox('Kecamatan',['Seluruh Kota']+KECAMATAN)
with c3:
    start = 2022 if indikator == 'Tempat Tidur Rumah Sakit' else 2020
    tahun = st.select_slider('Tahun detail',options=list(range(start,2026)),value=2025)

kpi('Jumlah terpilih',fmt(total_year(data,indikator,tahun,kecamatan)),f'{tahun} • {kecamatan}',TEAL)
st.subheader('Perubahan dari tahun ke tahun')
trend = annual_trend(data,indikator,kecamatan)
show_chart(px.line(trend,x='Tahun',y='Jumlah',markers=True,color_discrete_sequence=[TEAL]))

kategori = {
    'Tenaga Kesehatan':'Tenaga Kesehatan','Puskesmas':'Pelayanan',
    'Rumah Sakit':'Jenis Rumah Sakit',
    'Rumah Sakit Berdasarkan Kelas':'Kelas Rumah Sakit',
    'Rumah Sakit Berdasarkan Akreditasi':'Akreditasi Rumah Sakit',
    'Tempat Tidur Rumah Sakit':'Kelas Rumah Sakit',
    'Posyandu':'Kecamatan',
}[indikator]
raw = annual(data[indikator],tenaga=indikator=='Tenaga Kesehatan')
raw = raw[raw['Tahun']==tahun]
if kecamatan != 'Seluruh Kota':
    raw = raw[raw['Kecamatan']==kecamatan]
summary = raw.groupby(kategori,as_index=False)['Jumlah'].sum().sort_values('Jumlah',ascending=False)
st.subheader('Komposisi pada periode terpilih')
show_chart(px.bar(summary,x='Jumlah',y=kategori,orientation='h',color_discrete_sequence=[CORAL]))
st.dataframe(summary,hide_index=True,use_container_width=True)
if indikator == 'Rumah Sakit' or indikator.startswith('Rumah Sakit Berdasarkan'):
    st.caption('Ketiga klasifikasi RS merujuk pada fasilitas yang sama; jumlah antar-klasifikasi tidak dijumlahkan.')
