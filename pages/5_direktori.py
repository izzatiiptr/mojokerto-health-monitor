"""Direktori berdasarkan listing Google Maps; marker hanya untuk titik terverifikasi."""
import html
from urllib.parse import parse_qs, urlencode, urlparse

import folium
import streamlit as st
from streamlit_folium import st_folium

from src.config import AQI_LAT, AQI_LON, CORAL, KECAMATAN, TEAL
from src.data import load_directory
from src.visuals import hero, note, section


def maps_urls(row):
    """Buat tautan ke listing dan rute Google Maps memakai Place ID, tanpa butuh koordinat."""
    listing_url = str(row['Google_Maps_URL']).strip()
    params = parse_qs(urlparse(listing_url).query)
    place_id = (params.get('query_place_id') or [''])[0]
    destination = f"{row['Nama_Fasilitas']}, {row['Alamat']}"
    query = {'api': '1', 'destination': destination}
    if place_id:
        query['destination_place_id'] = place_id
    directions_url = 'https://www.google.com/maps/dir/?' + urlencode(query)
    return listing_url, directions_url


hero(
    'Peta & Direktori Kesehatan',
    'Temukan rumah sakit dan puskesmas di Kota Mojokerto, lalu buka lokasi atau rute melalui Google Maps.',
    'INTERACTIVE HEALTHCARE MAP',
)

df = load_directory()
st.caption('Alamat dan tautan mengikuti listing Google Maps. Filter kecamatan memakai pembagian administratif pada dataset.')

c1, c2, c3 = st.columns([1, 1, 1.4], gap='large')
with c1:
    jenis_list = sorted(x for x in df['Jenis_Fasilitas'].dropna().unique() if x)
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
    filtered = filtered[
        filtered['Nama_Fasilitas'].str.contains(cari, case=False, regex=False, na=False)
    ]

# Koordinat tidak boleh ditebak dari nama fasilitas. Hanya koordinat yang
# diperiksa terhadap pin Google Maps dan dicatat pada CSV yang akan dipetakan.
located = filtered.dropna(subset=['Latitude', 'Longitude']).copy()
for field in ['Nama_Fasilitas', 'Jenis_Fasilitas', 'Alamat', 'Sumber_Verifikasi']:
    located = located[located[field].str.strip().ne('')]
located = located[
    located['Latitude'].between(-7.60, -7.30)
    & located['Longitude'].between(112.30, 112.60)
]

left, right = st.columns([1, 1.85], gap='large')
with left:
    with st.container(border=True):
        section('Direktori Fasilitas')
        st.caption(f'{len(filtered)} fasilitas terdaftar · {len(located)} titik terpetakan')
        if filtered.empty:
            st.info('Tidak ada fasilitas yang sesuai dengan filter atau kata kunci.')
        else:
            # Daftar scrollable agar halaman peta tidak memanjang sepanjang 12 kartu.
            with st.container(height=560, border=False):
                for _, row in filtered.iterrows():
                    with st.container(border=True):
                        title = html.escape(row['Nama_Fasilitas'])
                        st.markdown(f'**{title}**')
                        st.caption(f"{row['Jenis_Fasilitas']} · {row['Kecamatan']}")
                        st.write(row['Alamat'])
                        maps_url, directions_url = maps_urls(row)
                        b1, b2 = st.columns(2, gap='small')
                        with b1:
                            if maps_url.startswith('https://www.google.com/maps/'):
                                st.link_button('🗺️ Google Maps', maps_url, use_container_width=True)
                        with b2:
                            st.link_button('📍 Petunjuk arah', directions_url, use_container_width=True)
                        if row.name not in located.index:
                            st.caption('Titik marker belum diverifikasi; lokasi dapat dibuka di Google Maps.')

with right:
    with st.container(border=True):
        section('Peta Interaktif Kota Mojokerto')
        center = (
            [float(located['Latitude'].mean()), float(located['Longitude'].mean())]
            if not located.empty else [AQI_LAT, AQI_LON]
        )
        fmap = folium.Map(
            location=center,
            zoom_start=13,
            tiles='OpenStreetMap',
            control_scale=True,
            prefer_canvas=True,
        )
        for _, row in located.iterrows():
            name = html.escape(row['Nama_Fasilitas'])
            address = html.escape(row['Alamat'])
            maps_url, directions_url = maps_urls(row)
            is_hospital = row['Jenis_Fasilitas'] == 'Rumah Sakit'
            marker_color = CORAL if is_hospital else TEAL
            popup = (
                '<div style="min-width:220px;font:13px Arial,sans-serif;line-height:1.6">'
                f'<strong>{name}</strong><br>{address}<br>'
                f'<a href="{html.escape(maps_url, quote=True)}" target="_blank" '
                'rel="noopener noreferrer">Lihat di Google Maps</a><br>'
                f'<a href="{html.escape(directions_url, quote=True)}" target="_blank" '
                'rel="noopener noreferrer">Petunjuk arah</a></div>'
            )
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=10,
                color='white',
                weight=3,
                fill=True,
                fill_color=marker_color,
                fill_opacity=1,
                tooltip=name,
                popup=folium.Popup(popup, max_width=300),
            ).add_to(fmap)

        st_folium(
            fmap, height=555, width=None,
            returned_objects=[], key='health_map_osm_v04',
        )
        st.caption('Peta dasar © OpenStreetMap contributors. Navigasi fasilitas dibuka melalui Google Maps.')
        if located.empty:
            st.info(
                'Daftar 12 fasilitas sudah tersedia. Marker belum ditampilkan karena koordinat pin '
                'Google Maps belum dimasukkan dan diverifikasi. Gunakan tombol Google Maps atau Petunjuk arah pada daftar.'
            )

note(
    'Direktori ini menggambarkan lokasi fasilitas, bukan jumlah historis. '
    'Perbedaan ejaan kecamatan pada Google Maps dan data administratif dicatat terpisah. '
    'Koordinat harus mengikuti pin Google Maps yang telah diperiksa, bukan titik perkiraan.'
)
