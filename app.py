"""Entrypoint Mojokerto Health Monitor. Jalankan: streamlit run app.py."""
import streamlit as st
from src.visuals import use_theme

st.set_page_config(
    page_title='Mojokerto Health Monitor',
    page_icon='🏥',
    layout='wide',
    initial_sidebar_state='expanded',
)
use_theme()

# Tetap memakai navigasi bawaan Streamlit agar perpindahan halaman menjaga state.
# Daftar menu kita letakkan manual setelah identitas aplikasi di dalam sidebar.
page_specs = [
    ('pages/1_beranda.py', 'Beranda', '🏠'),
    ('pages/2_tenaga_kesehatan.py', 'Tenaga Kesehatan', '👩‍⚕️'),
    ('pages/3_fasilitas_kapasitas.py', 'Fasilitas & Kapasitas', '🏥'),
    ('pages/4_distribusi.py', 'Analisis Distribusi', '📊'),
    ('pages/5_direktori.py', 'Peta & Direktori', '📍'),
]
pages = [
    st.Page(path, title=title, icon=icon, default=(i == 0))
    for i, (path, title, icon) in enumerate(page_specs)
]
nav = st.navigation(pages, position='hidden')

with st.sidebar:
    # Sidebar primer minimal setinggi layar. Tombol 112 didorong ke bagian
    # bawah dengan CSS; bagian sumber data berada SETELAH tombol tersebut.
    with st.container(key='sidebar_primary', border=False):
        st.markdown(
            '<div class="sidebar-brand">'
            '<div class="brand-mini">KOTA MOJOKERTO</div>'
            '<div class="brand-title">✚ MOJOKERTO<br>HEALTH MONITOR</div>'
            '<div class="brand-caption">Dashboard Informasi dan Analisis Kesehatan</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sidebar-menu-heading">MENU UTAMA</div>',
            unsafe_allow_html=True,
        )
        for page, (_, title, icon) in zip(pages, page_specs):
            st.page_link(page, label=title, icon=icon, use_container_width=True)

        st.markdown(
            '<a class="emergency-link" href="tel:112" '
            'aria-label="Buka aplikasi telepon untuk menghubungi 112">'
            '🚨 DARURAT 112</a>',
            unsafe_allow_html=True,
        )

    # Informasi sekunder berada di bawah area utama dan dapat digulir.
    with st.container(key='sidebar_secondary', border=False):
        st.markdown(
            '<div class="sidebar-meta-heading">INFORMASI DATA</div>',
            unsafe_allow_html=True,
        )
        st.caption('📅 Data historis: 2020–2025')
        st.caption('🌿 AQI: estimasi model atmosfer')
        st.caption('☎️ Tombol 112 membuka aplikasi telepon jika perangkat mendukung; tidak otomatis menelepon.')
        with st.expander('Sumber data & metodologi'):
            st.markdown(
                '**Data Kesehatan:** SATA JATIM (2020–2025).  \n'
                '**Analisis:** EDA, statistik deskriptif, HHI & Gini.  \n'
                '**Kualitas Udara:** Open-Meteo (US AQI; bukan ISPU).  \n'
                '**Catatan:** Dashboard ini bukan merupakan situs resmi Pemerintah Kota Mojokerto.'
            )

nav.run()
