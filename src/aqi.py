import requests
import streamlit as st
from src.config import AQI_LAT, AQI_LON

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_air_quality():
    response = requests.get(
        'https://air-quality-api.open-meteo.com/v1/air-quality',
        params={
            'latitude': AQI_LAT,
            'longitude': AQI_LON,
            'current': 'us_aqi,pm2_5,pm10',
            'hourly': 'us_aqi,pm2_5,pm10',
            'past_days': 1,
            'forecast_days': 1,
            'timezone': 'Asia/Jakarta',
        },
        timeout=12,
    )
    response.raise_for_status()
    return response.json()
