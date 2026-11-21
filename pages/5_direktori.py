"""Peta interaktif dengan marker hanya untuk lokasi yang sudah diisi dan diperiksa."""
import html
from urllib.parse import quote
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium
from src.data import load_directory
from src.config import KECAMATAN, AQI_LAT, AQI_LON
from src.visuals import hero, kpi, note, section

hero('Peta & Direktori Kesehatan',
     'Cari rumah sakit atau puskesmas, pilih marker, lalu buka petunjuk arah melalui Google Maps.',
     'INTERACTIVE HEALTHCARE MAP')

df = load_directory()
if df.empty:
    st.warning('Direktori fasilitas masih berupa template. Peta tetap dapat digunakan, tetapi belum ada marker fasilitas yang tervalidasi.')
else:
    st.info('Direktori adalah informasi lokasi fasilitas saat ini, bukan jumlah historis tahun 2025.')

c1, c2, c3 = st.columns([1, 1, 1.3])
with c1:
    jenis = st.selectbox('Jenis fasilitas', ['Semua'] + sorted(df['Jenis_Fasilitas'].dropna().unique().tolist()))
with c2:
    kec = st.selectbox('Kecamatan', ['Semua'] + KECAMATAN)
with c3:
    cari = st.text_input('Cari nama fasilitas', placeholder='Cari RS atau puskesmas...')

filtered = df.copy()
if jenis != 'Semua':
    filtered = filtered[filtered['Jenis_Fasilitas'] == jenis]
if kec != 'Semua':
    filtered = filtered[filtered['Kecamatan'] == kec]
if cari:
    filtered = filtered[filtered['Nama_Fasilitas'].str.contains(cari, case=False, regex=False, na=False)]

# Batas kewajaran untuk mendeteksi kesalahan masukan; bukan pengganti verifikasi lokasi.
located = filtered.dropna(subset=['Latitude', 'Longitude']).copy()
# Sumber dan alamat wajib terisi sebelum marker/navigasi dinyatakan siap.
for required in ['Nama_Fasilitas', 'Jenis_Fasilitas', 'Kecamatan', 'Alamat', 'Sumber_Verifikasi']:
    located = located[located[required].str.strip().ne('')]
located = located[
    located['Latitude'].between(-7.60, -7.30)
    & located['Longitude'].between(112.30, 112.60)
]
verified_rows = set(located.index)

left, right = st.columns([1, 1.55], gap='large')
with left:
    with st.container(border=True):
        section('Direktori Fasilitas')
        st.caption(f'{len(filtered)} fasilitas dalam daftar • {len(located)} siap ditampilkan pada peta')
        if filtered.empty:
            st.info('Belum ada fasilitas sesuai filter. Data lokasi dapat dilengkapi pada `data/direktori/fasilitas.csv`.')
        for _, row in filtered.iterrows():
            with st.container(border=True):
                st.markdown(f"**{html.escape(row['Nama_Fasilitas'])}**")
                st.caption(f"{row['Jenis_Fasilitas']} · {row['Kecamatan']}")
                st.write(row['Alamat'] or 'Alamat belum dilengkapi')
                if row.name in verified_rows:
                    loc = f"{row['Latitude']},{row['Longitude']}"
                    url = f'https://www.google.com/maps/dir/?api=1&destination={quote(loc)}'
                    st.link_button('📍 Petunjuk Arah', url, use_container_width=True)
                else:
                    st.caption('Navigasi belum tersedia: alamat, koordinat, atau sumber verifikasi belum lengkap.')

with right:
    with st.container(border=True):
        section('Peta Interaktif Kota Mojokerto')
        if located.empty:
            st.caption('Peta dasar tanpa marker. Lokasi fasilitas belum tersedia atau tidak cocok dengan filter.')
        center = ([located['Latitude'].mean(), located['Longitude'].mean()]
                  if not located.empty else [AQI_LAT, AQI_LON])
        fmap = folium.Map(location=center, zoom_start=13, tiles='CartoDB positron', control_scale=True)
        for _, row in located.iterrows():
            name = html.escape(row['Nama_Fasilitas'])
            address = html.escape(row['Alamat'])
            is_hospital = 'rumah sakit' in row['Jenis_Fasilitas'].lower() or row['Jenis_Fasilitas'].lower().startswith('rs')
            marker_color = 'red' if is_hospital else 'green'
            ico = 'plus-sign' if is_hospital else 'heart'
            loc = f"{row['Latitude']},{row['Longitude']}"
            url = f'https://www.google.com/maps/dir/?api=1&destination={quote(loc)}'
            popup = (
                f'<div style="font-family:sans-serif;min-width:195px">'
                f'<strong>{name}</strong><br>{address}<br><br>'
                f'<a href="{url}" target="_blank" rel="noopener noreferrer">📍 Petunjuk Arah</a>'
                f'</div>'
            )
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                tooltip=name,
                popup=folium.Popup(popup, max_width=270),
                icon=folium.Icon(color=marker_color, icon=ico)
            ).add_to(fmap)
        st_folium(fmap, height=520, width=None, returned_objects=[], key='health_map')
        st.caption('Peta dasar: OpenStreetMap/Carto. Arah navigasi dibuka pada Google Maps.')

note('Jumlah historis fasilitas pada Project 1 tidak mengandung koordinat bangunan. Marker hanya akan ditampilkan setelah pengumpulan dan verifikasi alamat serta titik lokasi masing-masing fasilitas.')
