"""Entrypoint Streamlit untuk GitHub dan Streamlit Community Cloud."""
import streamlit as st
from src.visuals import use_theme

st.set_page_config(
    page_title='Mojokerto Health Monitor', page_icon='🏥',
    layout='wide', initial_sidebar_state='expanded'
)
use_theme()

with st.sidebar:
    st.markdown('## 🏥 MOJOKERTO')
    st.markdown('**HEALTH MONITOR**')
    st.caption('Dashboard Informasi & Analisis Kesehatan')
    st.divider()
    st.markdown('<a class="emergency-link" href="tel:112">🚨 HUBUNGI 112</a>', unsafe_allow_html=True)
    st.caption('Membuka dialer di perangkat yang mendukung; tidak menelepon otomatis.')
    st.divider()
    st.caption('📊 Data historis: 2020–2025')
    st.caption('🌿 Kualitas udara: estimasi model')
    st.caption('Proyek akademik, bukan layanan resmi pemerintah.')

pages = [
    st.Page('pages/1_beranda.py', title='Beranda', icon='🏠', default=True),
    st.Page('pages/2_sumber_daya.py', title='Sumber Daya Kesehatan', icon='📊'),
    st.Page('pages/3_distribusi.py', title='Analisis Distribusi', icon='📈'),
    st.Page('pages/4_direktori.py', title='Peta & Direktori', icon='🗺️'),
    st.Page('pages/5_kualitas_udara.py', title='Kualitas Udara', icon='🌿'),
]
st.navigation(pages).run()
