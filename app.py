"""Jalankan dari root repository: streamlit run app.py"""
import streamlit as st
from src.visuals import use_theme

st.set_page_config(
    page_title='Mojokerto Health Monitor', page_icon='🏥',
    layout='wide', initial_sidebar_state='expanded',
)
use_theme()

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand"><div class="brand-mini">KOTA MOJOKERTO</div>'
        '<div class="brand-title">✚ MOJOKERTO<br>HEALTH MONITOR</div>'
        '<div class="brand-caption">Dashboard Informasi dan Analisis Kesehatan</div></div>',
        unsafe_allow_html=True
    )

nav = st.navigation([
    st.Page('pages/1_beranda.py', title='Beranda', icon='🏠', default=True),
    st.Page('pages/2_tenaga_kesehatan.py', title='Tenaga Kesehatan', icon='👩‍⚕️'),
    st.Page('pages/3_fasilitas_kapasitas.py', title='Fasilitas & Kapasitas', icon='🏥'),
    st.Page('pages/4_distribusi.py', title='Analisis Distribusi', icon='📊'),
    st.Page('pages/5_direktori.py', title='Peta & Direktori', icon='📍'),
])

with st.sidebar:
    st.markdown('---')
    st.markdown('<a class="emergency-link" href="tel:112" aria-label="Buka panggilan darurat 112">🚨 DARURAT 112</a>',unsafe_allow_html=True)
    st.caption('Membuka aplikasi telepon jika didukung perangkat; tidak melakukan panggilan otomatis.')
    st.markdown('---')
    st.caption('📅 Data historis: 2020–2025')
    st.caption('🌿 AQI: estimasi dari model atmosfer')
    with st.expander('Sumber data & metodologi'):
        st.markdown('''**Historis:** SATA JATIM, hasil olahan Project 1.  
**Indeks:** HHI & Gini untuk jumlah absolut antar-kecamatan.  
**AQI:** Open-Meteo (US AQI; bukan ISPU).  
**Batasan:** bukan layanan resmi Pemkot Mojokerto.''')

nav.run()
