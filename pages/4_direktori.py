import html
import pandas as pd
from urllib.parse import quote
import streamlit as st
from folium import Map,Marker,Popup,Icon
from streamlit_folium import st_folium
from src.data import load_directory
from src.config import KECAMATAN
from src.visuals import hero

hero('Peta & Direktori Fasilitas',
     'Pilih fasilitas untuk melihat alamat dan membuka navigasi Google Maps.',
     'DIREKTORI • LOKASI TERVERIFIKASI')
df = load_directory()
if df.empty:
    st.warning('Data direktori belum diisi. Nama, alamat, dan koordinat fasilitas perlu diverifikasi sebelum dipublikasikan.')
    st.code('data/direktori/fasilitas.csv',language=None)
    st.stop()

c1,c2 = st.columns(2)
with c1:
    jenis = st.selectbox('Jenis fasilitas',['Semua']+sorted(df['Jenis_Fasilitas'].unique().tolist()))
with c2:
    kecamatan = st.selectbox('Kecamatan',['Semua']+KECAMATAN)
cari = st.text_input('Cari nama fasilitas',placeholder='Nama puskesmas atau rumah sakit...')
filtered = df.copy()
if jenis != 'Semua': filtered = filtered[filtered['Jenis_Fasilitas']==jenis]
if kecamatan != 'Semua': filtered = filtered[filtered['Kecamatan']==kecamatan]
if cari: filtered = filtered[filtered['Nama_Fasilitas'].str.contains(cari,case=False,regex=False,na=False)]
st.caption(f'{len(filtered)} fasilitas sesuai filter')
left,right = st.columns([1.4,1],gap='large')
with left:
    located = filtered.dropna(subset=['Latitude','Longitude'])
    located = located[located['Latitude'].between(-7.60,-7.30)&located['Longitude'].between(112.30,112.60)]
    if located.empty:
        st.info('Belum ada titik koordinat tervalidasi untuk pilihan ini.')
    else:
        fmap = Map(location=[located['Latitude'].mean(),located['Longitude'].mean()],zoom_start=12,tiles='CartoDB positron')
        for _,row in located.iterrows():
            name = html.escape(row['Nama_Fasilitas'])
            address = html.escape(row['Alamat'])
            location = f"{row['Latitude']},{row['Longitude']}"
            # URL peta menggunakan koordinat yang sudah divalidasi; pengguna memilih rute setelah Google Maps terbuka.
            url = f'https://www.google.com/maps/search/?api=1&query={quote(location)}'
            popup = f'<b>{name}</b><br>{address}<br><a href="{url}" target="_blank" rel="noopener noreferrer">📍 Buka Google Maps</a>'
            Marker([row['Latitude'],row['Longitude']],popup=Popup(popup,max_width=300),icon=Icon(color='green')).add_to(fmap)
        st_folium(fmap,height=470,width=None,returned_objects=[])
with right:
    for _,row in filtered.iterrows():
        with st.container(border=True):
            st.markdown(f"**{row['Nama_Fasilitas']}**")
            st.caption(f"{row['Jenis_Fasilitas']} • {row['Kecamatan']}")
            st.write(row['Alamat'] or 'Alamat belum tersedia')
            url = row['Google_Maps_URL']
            if not url and pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                url = f"https://www.google.com/maps/search/?api=1&query={row['Latitude']},{row['Longitude']}"
            if url.startswith('https://'):
                st.link_button('📍 Buka Google Maps',url,use_container_width=True)
            else:
                st.caption('Lokasi digital belum terverifikasi.')
