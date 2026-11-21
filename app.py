"""Entrypoint Mojokerto Health Monitor. Jalankan: streamlit run app.py"""
import streamlit as st
from src.visuals import use_theme

st.set_page_config(
    page_title='Mojokerto Health Monitor',
    page_icon='🏥',
    layout='wide',
    initial_sidebar_state='expanded',
)
use_theme()

# Navigasi bawaan selalu berada di paling atas sidebar. Matikan tampilannya
# agar identitas aplikasi bisa ditempatkan di atas daftar menu.
page_specs = [
    ('pages/1_beranda.py', 'Beranda', '🏠'),
    ('pages/2_tenaga_kesehatan.py', 'Tenaga Kesehatan', '👩‍⚕️'),
    ('pages/3_fasilitas_kapasitas.py', 'Fasilitas & Kapasitas', '🏥'),
    ('pages/4_distribusi.py', 'Analisis Distribusi', '📊'),
    ('pages/5_direktori.py', 'Peta & Direktori', '📍'),
]
pages = [st.Page(path, title=title, icon=icon, default=(i == 0))
         for i, (path, title, icon) in enumerate(page_specs)]
nav = st.navigation(pages, position='hidden')

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">'
        '<div class="brand-mini">KOTA MOJOKERTO</div>'
        '<div class="brand-title">✚ MOJOKERTO<br>HEALTH MONITOR</div>'
        '<div class="brand-caption">Dashboard Informasi dan Analisis Kesehatan</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sidebar-menu-heading">MENU UTAMA</div>', unsafe_allow_html=True)
    for page, (_, title, icon) in zip(pages, page_specs):
        st.page_link(page, label=title, icon=icon, use_container_width=True)

    st.divider()
    st.markdown(
        '<a class="emergency-link" href="tel:112" '
        'aria-label="Buka panggilan darurat 112">🚨 DARURAT 112</a>',
        unsafe_allow_html=True,
    )
    st.caption('Membuka aplikasi telepon jika didukung perangkat; tidak melakukan panggilan otomatis.')
    st.divider()
    st.caption('📅 Data historis: 2020–2025')
    st.caption('🌿 AQI: estimasi dari model atmosfer')
    with st.expander('Sumber data & metodologi'):
        st.markdown(
            '**Historis:** SATA JATIM, hasil olahan Project 1.  \n'
            '**Indeks:** HHI & Gini untuk jumlah absolut antar-kecamatan.  \n'
            '**AQI:** Open-Meteo (US AQI; bukan ISPU).  \n'
            '**Batasan:** bukan layanan resmi Pemkot Mojokerto.'
        )

nav.run()
