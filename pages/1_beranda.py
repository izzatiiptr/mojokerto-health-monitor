import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from src.aqi import fetch_air_quality, aqi_category
from src.data import load_health_data, annual_trend, total_year
from src.config import TEAL, MUTED_TEAL, PEACH, CORAL, PALETTE
from src.visuals import hero, kpi, fmt, note, show_chart, section

hero('Kesehatan Mojokerto, lebih mudah dipahami',
     'Pantau sumber daya kesehatan, jelajahi fasilitas pelayanan, dan lihat estimasi kualitas udara dalam satu dashboard.',
     'DASHBOARD KOTA MOJOKERTO • DATA HISTORIS 2020–2025')

data = load_health_data()
section('Ringkasan Sumber Daya • 2025', 'Tenaga kesehatan menggunakan Semester II. Lima indikator memiliki definisi dan satuan berbeda.')
items = [
    ('Tenaga Kesehatan', 'Tenaga Kesehatan', 'orang • Semester II', TEAL),
    ('Puskesmas', 'Puskesmas', 'unit', MUTED_TEAL),
    ('Rumah Sakit', 'Rumah Sakit', 'unit', CORAL),
    ('Posyandu', 'Posyandu', 'unit', PEACH),
    ('Tempat Tidur RS', 'Tempat Tidur Rumah Sakit', 'tempat tidur', TEAL),
]
for col, (label, key, suffix, color) in zip(st.columns(5, gap='small'), items):
    with col:
        kpi(label, fmt(total_year(data, key, 2025)), suffix, color)

st.write('')
left, right = st.columns([1.5, 1], gap='large')
with left:
    with st.container(border=True):
        section('Perkembangan Tenaga Kesehatan', 'Jumlah tenaga kesehatan pada Semester II setiap tahun.')
        trend = annual_trend(data, 'Tenaga Kesehatan')
        fig = px.area(trend, x='Tahun', y='Jumlah', markers=True, color_discrete_sequence=[TEAL])
        fig.update_traces(line_width=3, fillcolor='rgba(95,168,160,0.20)')
        fig.update_xaxes(dtick=1)
        show_chart(fig, height=315)
    with st.container(border=True):
        section('Temukan Fasilitas Kesehatan')
        st.write('Buka peta interaktif untuk mencari rumah sakit atau puskesmas dan melanjutkan navigasi melalui Google Maps.')
        st.page_link('pages/5_direktori.py', label='📍 Buka Peta & Direktori', use_container_width=True)
        st.caption('Marker tersedia setelah koordinat fasilitas diverifikasi dan diisi ke direktori.')

with right:
    with st.container(border=True):
        section('🌿 Kualitas Udara Kota Mojokerto')
        st.caption('US AQI • estimasi model Open-Meteo (bukan pengukuran sensor)')
        try:
            payload = fetch_air_quality()
            current = payload.get('current') or {}
            aqi = current.get('us_aqi')
            if aqi is None:
                st.info('Nilai AQI belum tersedia dari penyedia data.')
            else:
                kpi('US AQI', str(aqi), aqi_category(aqi), MUTED_TEAL)
            c1, c2 = st.columns(2)
            with c1:
                st.metric('PM2.5', f"{current.get('pm2_5', '—')} µg/m³")
            with c2:
                st.metric('PM10', f"{current.get('pm10', '—')} µg/m³")
            st.caption(f"Waktu data: {current.get('time','tidak tersedia')} WIB • cache 30 menit")
            with st.expander('📈 Lihat detail dan tren AQI per jam'):
                hourly = pd.DataFrame(payload.get('hourly') or {})
                if {'time', 'us_aqi', 'pm2_5', 'pm10'}.issubset(hourly.columns):
                    hourly['time'] = pd.to_datetime(hourly['time'])
                    metric = st.selectbox('Parameter', ['us_aqi', 'pm2_5', 'pm10'],
                                          format_func=lambda x: {'us_aqi':'US AQI','pm2_5':'PM2.5','pm10':'PM10'}[x])
                    fig = px.line(hourly, x='time', y=metric, color_discrete_sequence=[TEAL])
                    show_chart(fig, height=250)
                    st.caption('Deret ini dapat memuat estimasi periode sebelumnya dan prakiraan mendatang.')
                else:
                    st.info('Data tren per jam belum tersedia.')
        except (requests.RequestException, KeyError, TypeError, ValueError):
            st.warning('Kualitas udara belum dapat dimuat. Statistik historis tetap dapat diakses.')
        st.caption('US AQI tidak sama dengan ISPU Indonesia. Titik API mewakili area kota, bukan lokasi sensor.')

note('Data 2025 bukan kondisi real-time. HHI dan Gini menjelaskan konsentrasi/ketimpangan jumlah absolut antar-kecamatan, bukan kecukupan layanan menurut kebutuhan penduduk.')
