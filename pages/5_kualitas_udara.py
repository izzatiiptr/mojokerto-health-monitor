import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from src.aqi import fetch_air_quality
from src.config import TEAL,CORAL,AMBER
from src.visuals import hero,kpi,note,show_chart

hero('Kualitas Udara Kota Mojokerto',
     'Estimasi kualitas udara terbaru dari Open-Meteo Air Quality API.',
     'LINGKUNGAN & KESEHATAN')
note('US AQI dan konsentrasi PM2.5/PM10 adalah estimasi berbasis model atmosfer, bukan pembacaan sensor langsung. Berbeda dari ISPU Indonesia.')
try:
    payload = fetch_air_quality()
    current = payload.get('current',{})
    cols = st.columns(3)
    with cols[0]: kpi('US AQI',current.get('us_aqi','N/A'),'Estimasi kualitas udara',TEAL)
    with cols[1]: kpi('PM2.5',current.get('pm2_5','N/A'),'µg/m³',CORAL)
    with cols[2]: kpi('PM10',current.get('pm10','N/A'),'µg/m³',AMBER)
    st.caption(f"Waktu data model: {current.get('time','tidak tersedia')} (Asia/Jakarta). Cache permintaan: 30 menit.")
    hourly = pd.DataFrame(payload['hourly'])
    hourly['time'] = pd.to_datetime(hourly['time'])
    metric = st.selectbox('Indikator per jam',['us_aqi','pm2_5','pm10'])
    st.subheader('Tren per jam')
    show_chart(px.line(hourly,x='time',y=metric,color_discrete_sequence=[TEAL]))
    st.caption('Grafik memuat periode historis dan prakiraan model; bukan rekaman sensor real-time.')
except (requests.RequestException, KeyError, ValueError, TypeError) as exc:
    st.warning('Data kualitas udara belum dapat ditampilkan. Coba lagi saat API tersedia.')
    st.caption(f'Keterangan: {type(exc).__name__}')
