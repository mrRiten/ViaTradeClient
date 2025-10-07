import asyncio
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from domain.entity import User
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.repositories.sqlite_config import sqlite_url

import streamlit as st
from view.singal.signal_tab import show_signals_tab
from view.trade.trade_tab import show_trade_tab

st.set_page_config(
    page_title="ViaTrade",
    page_icon="🧮",
    layout="centered"
)

# CSS для увеличения ширины контейнера
st.markdown("""
    <style>
        .block-container {
            max-width: 50rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("VitTrade – инвестиционный анализ")

tab1, tab2 = st.tabs(["Сигналы", "Анализ сделок"])

with tab1:
    show_signals_tab()

with tab2:
    show_trade_tab()
