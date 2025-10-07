import os
import streamlit as st
from datetime import datetime, timedelta
from vittrade import InvestmentService


@st.cache_data(show_spinner="Загрузка данных с биржи...")
def load_signals():
    service = InvestmentService()
    invest_ids = service.load_invest_ids()

    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    start_str, end_str = start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    results = service.run_parallel_processing(invest_ids, start_str, end_str)
    return service, invest_ids, results


def show_signals_tab():
    st.header("📊 Инвестиционные сигналы")

    service, invest_ids, results = load_signals()

    # --- агрегированные сигналы ---
    buy, sell = service.get_today_signals(results)

    st.subheader("Сводка сигналов на последнюю дату")
    st.write("🟢 Buy:", ", ".join(buy) if buy else "нет")
    st.write("🔴 Sell:", ", ".join(sell) if sell else "нет")

    # --- последние 5 строк по каждому тикеру ---
    st.subheader("Последние 5 дней по каждому инструменту")
    recent = service.get_recent_data(invest_ids, days=5)
    for invest_id in invest_ids:
        df = recent.get(invest_id)
        if df is None or df.empty:
            st.warning(f"{invest_id}: нет данных")
            continue
        st.markdown(f"**{invest_id}**")
        st.dataframe(df[[
            "TRADEDATE", "CLOSE", "RSI", "MACD", "EMA_12", "EMA_26",
            "ADX", "Stoch_K", "Stoch_D", "ATR", "Signal"
        ]])

    # --- Кнопка для открытия директории ---
    if st.button("📂 Открыть папку с CSV"):
        folder_path = os.path.abspath("data")
        os.startfile(folder_path)  # работает в Windows
