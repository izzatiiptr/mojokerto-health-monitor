import streamlit as st
import plotly.express as px
from src.data import load_health_data, total_year, annual_trend
from src.aqi import fetch_air_quality
from src.config import TEAL, CORAL, NAVY, AMBER
from src.visuals import hero, kpi, note, fmt, show_chart
import requests

hero('Kesehatan Kota Mojokerto, dalam satu ruang informasi',
     'Statistik sumber daya pelayanan kesehatan 2020–2025, lokasi fasilitas, dan estimasi kualitas udara.')
data = load_health_data()
items = [
    ('Tenaga kesehatan','Tenaga Kesehatan','Semester II 2025',TEAL),
    ('Puskesmas','Puskesmas','2025',NAVY),
    ('Rumah sakit','Rumah Sakit','2025',CORAL),
    ('Posyandu','Posyandu','2025',AMBER),
    ('Tempat tidur RS','Tempat Tidur Rumah Sakit','2025',TEAL),
]
for col, (label,key,sub,color) in zip(st.columns(5),items):
    with col:
        kpi(label, fmt(total_year(data,key,2025)),sub,color)

left, right = st.columns([2.1,1],gap='large')
with left:
    st.subheader('Tren tenaga kesehatan')
    df = annual_trend(data,'Tenaga Kesehatan')
    show_chart(px.area(df,x='Tahun',y='Jumlah',markers=True,color_discrete_sequence=[TEAL]))
    st.caption('Angka tahunan tenaga kesehatan menggunakan Semester II; kedua semester tidak dijumlahkan.')
with right:
    st.subheader('Kualitas udara (US AQI)')
    try:
        cur = fetch_air_quality().get('current',{})
        if cur.get('us_aqi') is None:
            st.info('Estimasi AQI belum tersedia dari sumber API.')
        else:
            st.metric('US AQI • estimasi model',str(cur['us_aqi']))
            st.caption(f"Waktu data: {cur.get('time','tidak tersedia')} (Asia/Jakarta)")
    except (requests.RequestException,ValueError,KeyError,TypeError):
        st.info('API kualitas udara sedang tidak dapat diakses.')
    st.caption('Open-Meteo • bukan pengukuran sensor langsung di Mojokerto.')

note('HHI/Gini mengukur konsentrasi dan ketimpangan jumlah absolut antar-kecamatan, bukan kecukupan atau kesetaraan akses kesehatan.')
