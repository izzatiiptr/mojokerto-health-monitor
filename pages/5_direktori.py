"""Peta interaktif menggunakan OpenStreetMap tanpa kunci API CARTO."""
import html
from urllib.parse import quote
import folium
import streamlit as st
from streamlit_folium import st_folium
from src.data import load_directory
from src.config import KECAMATAN, AQI_LAT, AQI_LON, TEAL, CORAL
from src.visuals import hero, note, section

hero('Peta & Direktori Kesehatan',
     'Cari rumah sakit atau puskesmas, pilih marker, lalu buka petunjuk arah melalui Google Maps.',
     'INTERACTIVE HEALTHCARE MAP')

df = load_directory()
if df.empty:
    st.info('Peta Kota Mojokerto tersedia. Marker fasilitas akan muncul setelah koordinat dan sumber lokasinya dilengkapi di direktori.')
else:
    st.caption('Direktori menampilkan lokasi fasilitas saat ini, bukan angka historis 2025.')

c1, c2, c3 = st.columns([1, 1, 1.4], gap='large')
with c1:
    jenis_list = sorted(j for j in df['Jenis_Fasilitas'].dropna().unique() if j)
    jenis = st.selectbox('Jenis fasilitas', ['Semua'] + jenis_list)
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

# Koordinat yang masuk akal tidak otomatis benar. Hanya data dengan sumber dan alamat
# terisi yang boleh menjadi marker. Verifikasi sumber dilakukan saat kurasi CSV.
located = filtered.dropna(subset=['Latitude', 'Longitude']).copy()
for required in ['Nama_Fasilitas', 'Jenis_Fasilitas', 'Kecamatan', 'Alamat', 'Sumber_Verifikasi']:
    located = located[located[required].str.strip().ne('')]
located = located[
    located['Latitude'].between(-7.60, -7.30) &
    located['Longitude'].between(112.30, 112.60)
]
verified_rows = set(located.index)

left, right = st.columns([1, 2.0], gap='large')
with left:
    with st.container(border=True):
        section('Direktori Fasilitas')
        st.caption(f'{len(filtered)} fasilitas dalam daftar • {len(located)} lokasi siap dipetakan')
        if filtered.empty:
            st.info('Data fasilitas belum tersedia atau tidak sesuai filter. Isi `data/direktori/fasilitas.csv` setelah verifikasi sumber.')
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
                    st.caption('Navigasi belum tersedia: lokasi belum terverifikasi.')

with right:
    with st.container(border=True):
        section('Peta Interaktif Kota Mojokerto')
        # CARTO Positron tidak lagi dapat diandalkan tanpa API key (tile dapat
        # bertuliskan API KEY REQUIRED). Gunakan layer OpenStreetMap langsung.
        center = ([located['Latitude'].mean(), located['Longitude'].mean()]
                  if not located.empty else [AQI_LAT, AQI_LON])
        fmap = folium.Map(location=center, zoom_start=13, tiles='OpenStreetMap',
                          control_scale=True, prefer_canvas=True)
        for _, row in located.iterrows():
            name = html.escape(row['Nama_Fasilitas'])
            address = html.escape(row['Alamat'])
            kategori = row['Jenis_Fasilitas'].lower()
            is_hospital = 'rumah sakit' in kategori or kategori.startswith('rs')
            color = CORAL if is_hospital else TEAL
            loc = f"{row['Latitude']},{row['Longitude']}"
            url = f'https://www.google.com/maps/dir/?api=1&destination={quote(loc)}'
            popup = (
                '<div style="font:14px Arial,sans-serif;min-width:210px;line-height:1.5">'
                f'<strong>{name}</strong><br>{address}<br><br>'
                f'<a href="{url}" target="_blank" rel="noopener noreferrer">📍 Petunjuk Arah</a>'
                '</div>'
            )
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=10, color='white', weight=3, fill=True, fill_color=color,
                fill_opacity=1, tooltip=name, popup=folium.Popup(popup, max_width=280),
            ).add_to(fmap)
        st_folium(fmap, height=550, width=None, returned_objects=[], key='health_map_osm')
        st.caption('Peta dasar: © OpenStreetMap contributors. Zoom dan geser tersedia. Peta membutuhkan koneksi internet.')
        if located.empty:
            st.info('Belum ada marker karena CSV direktori belum berisi koordinat fasilitas yang diverifikasi. Peta dasar tetap dapat digunakan.')

note('Jumlah historis fasilitas pada Project 1 tidak mengandung titik lokasi bangunan. Pengisian nama, alamat, koordinat, dan sumber verifikasi merupakan pekerjaan terpisah sebelum direktori dapat digunakan untuk navigasi.')
