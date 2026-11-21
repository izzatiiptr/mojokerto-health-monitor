"""Komponen presentasi ringan yang dapat digunakan ulang di semua halaman."""
import html
import streamlit as st
from src.config import ROOT, DARK, MUTED_TEAL


def use_theme():
    css = (ROOT / 'assets' / 'styles.css').read_text(encoding='utf-8')
    st.markdown('<style>' + css + '</style>', unsafe_allow_html=True)


def hero(title, subtitle, badge='MOJOKERTO • HEALTH MONITOR'):
    st.markdown(
        f'<section class="hero"><div class="hero-copy">'
        f'<span class="hero-tag">{html.escape(badge)}</span>'
        f'<h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p>'
        '</div><div class="hero-art" aria-hidden="true">'
        '<span class="art-blob"></span><span class="art-circle">✚</span>'
        '<span class="art-small">●</span></div></section>',
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
    st.markdown(f'<div class="note">{html.escape(str(text))}</div>', unsafe_allow_html=True)


def fmt(number):
    return '—' if number is None else f'{int(number):,}'.replace(',', '.')


def section(title, caption=None):
    st.markdown(f'<h3 class="section-title">{html.escape(title)}</h3>', unsafe_allow_html=True)
    if caption:
        st.caption(caption)


def show_chart(fig, height=340):
    fig.update_layout(
        height=height,
        font_family='Plus Jakarta Sans, Arial', font_color=DARK,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=22, b=16),
        legend_title_text='',
        hoverlabel=dict(bgcolor='white'),
    )
    fig.update_yaxes(gridcolor='#e6e7df', zeroline=False)
    fig.update_xaxes(gridcolor='#f2eee8')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
