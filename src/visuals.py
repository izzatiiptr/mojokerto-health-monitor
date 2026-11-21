import html
import streamlit as st
from src.config import ROOT, NAVY

def use_theme():
    css = (ROOT / 'assets' / 'styles.css').read_text(encoding='utf-8')
    st.markdown('<style>' + css + '</style>', unsafe_allow_html=True)

def hero(title, subtitle, badge='MOJOKERTO • HEALTH MONITOR'):
    st.markdown(
        f'<div class="hero"><small>{html.escape(badge)}</small>'
        f'<h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',
        unsafe_allow_html=True
    )

def kpi(label, value, subtitle, accent):
    st.markdown(
        f'<div class="kpi" style="--accent:{accent}">'
        f'<div class="kpi-label">{html.escape(str(label))}</div>'
        f'<div class="kpi-value">{html.escape(str(value))}</div>'
        f'<div class="kpi-sub">{html.escape(str(subtitle))}</div></div>',
        unsafe_allow_html=True
    )

def note(text):
    st.markdown(f'<div class="note">{html.escape(text)}</div>', unsafe_allow_html=True)

def fmt(number):
    return 'Belum ada data' if number is None else f'{int(number):,}'.replace(',', '.')

def show_chart(fig):
    fig.update_layout(
        font_family='Plus Jakarta Sans, Arial', font_color=NAVY,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10,r=10,t=25,b=25),
        legend_title_text=''
    )
    fig.update_yaxes(gridcolor='#e3eeee', zeroline=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
