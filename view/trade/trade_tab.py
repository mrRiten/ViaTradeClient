import streamlit as st
import asyncio
from datetime import datetime
import pandas as pd

from domain.entity import Trade
from infrastructure.repositories.sqlite_config import SessionLocal
from infrastructure.repositories.trade import TradeRepository
from infrastructure.repositories.tradecode import TradeCodeRepository
from infrastructure.repositories.tradetype import TradeTypeRepository


def show_trade_tab():
    st.header("📄 Анализ сделок (локальная БД)")
    if "init_done" not in st.session_state:
        asyncio.run(_init_db_session())

    asyncio.run(_show_current_trades())
    asyncio.run(_start_investment_form())
    asyncio.run(_end_investment_form())
    asyncio.run(_add_trade_form())
    asyncio.run(_edit_trade_form())
    asyncio.run(_delete_trade_form())


# ---------- Инициализация ----------
async def _init_db_session():
    st.session_state.session = SessionLocal()
    st.session_state.trade_repo = TradeRepository(st.session_state.session)
    st.session_state.tradecode_repo = TradeCodeRepository(st.session_state.session)
    st.session_state.tradetype_repo = TradeTypeRepository(st.session_state.session)
    st.session_state.init_done = True


# ---------- Просмотр ----------
async def _show_current_trades():
    trades = await st.session_state.trade_repo.get_all()
    if not trades:
        st.info("Нет сделок в базе данных.")
        return

    df = pd.DataFrame([
        {
            "ID": t.id,
            "DateOpen": t.date_open.strftime("%d.%m.%Y"),
            "DateClose": t.date_close.strftime("%d.%m.%Y") if t.date_close else "",
            "TradeOpen": t.trade_open,
            "TradeClose": t.trade_close,
            "NetIncome": t.net_income,
            "Count": t.count,
            "Type": t.trade_type.name if t.trade_type else "",
            "Code": t.trade_code.exchange_id if t.trade_code else "",
        }
        for t in trades
    ])
    st.dataframe(df)


# ---------- Начало инвестиции ----------
async def _start_investment_form():
    with st.expander("🚀 Начать инвестицию"):
        with st.form("start_investment"):
            date_open = st.date_input("Дата открытия", datetime.now()).strftime("%Y-%m-%d")
            trade_open = st.number_input("TradeOpen", min_value=0.0, step=0.01)
            count = st.number_input("Count", min_value=1, step=1)

            types = await st.session_state.tradetype_repo.get_all()
            type_options = {t.name: t.id for t in types}
            trade_type = st.selectbox("Тип", list(type_options.keys()))

            codes = await st.session_state.tradecode_repo.get_all()
            code_options = {c.exchange_id: c.id for c in codes}
            trade_code = st.selectbox("Код", list(code_options.keys()))

            user_id = 1
            submit = st.form_submit_button("Начать")

            if submit:
                trade = Trade(
                    date_open=datetime.strptime(date_open, "%Y-%m-%d"),
                    date_close=None,
                    trade_open=trade_open,
                    trade_close=None,
                    net_income=None,
                    count=count,
                    trade_type_id=type_options[trade_type],
                    trade_code_id=code_options[trade_code],
                    user_id=user_id,
                )
                await st.session_state.trade_repo.add(trade)
                st.success("Инвестиция начата!")
                st.rerun()


# ---------- Закрытие сделки ----------
async def _end_investment_form():
    with st.expander("✅ Закончить инвестицию"):
        trades = await st.session_state.trade_repo.get_all()
        open_trades = [t for t in trades if t.date_close is None]

        if not open_trades:
            st.info("Нет открытых сделок для завершения.")
            return

        trade_dict = {f"{t.id} | {t.trade_code.exchange_id}": t.id for t in open_trades}
        selected_key = st.selectbox("Выберите сделку", list(trade_dict.keys()))
        selected_id = trade_dict[selected_key]

        trade_close = st.number_input("TradeClose", min_value=0.0, step=0.01)
        date_close = datetime.now()
        submit = st.button("Закрыть")

        if submit:
            trade = await st.session_state.trade_repo.get_by_id(selected_id)
            trade.trade_close = trade_close
            trade.date_close = date_close
            if trade.trade_open:
                if trade.trade_type.name.lower() == "buy":
                    trade.net_income = round(((trade_close - trade.trade_open) / trade.trade_open) * 100, 2)
                else:
                    trade.net_income = round(((trade.trade_open - trade_close) / trade.trade_open) * 100, 2)

            await st.session_state.trade_repo.update(
                trade.id,
                trade_close=trade.trade_close,
                date_close=trade.date_close,
                net_income=trade.net_income,
            )
            st.success("Сделка завершена!")
            st.rerun()


# ---------- Добавление вручную ----------
async def _add_trade_form():
    with st.expander("➕ Добавить сделку (ручное CRUD)"):
        with st.form("add_trade"):
            date_open = st.date_input("Дата открытия", datetime.now()).strftime("%Y-%m-%d")
            date_close = st.text_input("Дата закрытия (может быть пусто)")
            trade_open = st.number_input("TradeOpen", min_value=0.0, step=0.01)
            trade_close = st.text_input("TradeClose")
            net_income = st.text_input("NetIncome")
            count = st.number_input("Count", min_value=1, step=1)

            types = await st.session_state.tradetype_repo.get_all()
            type_options = {t.name: t.id for t in types}
            trade_type = st.selectbox("Тип", list(type_options.keys()))

            codes = await st.session_state.tradecode_repo.get_all()
            code_options = {c.exchange_id: c.id for c in codes}
            trade_code = st.selectbox("Код", list(code_options.keys()))

            submit = st.form_submit_button("Добавить")

            if submit:
                trade = Trade(
                    date_open=datetime.strptime(date_open, "%Y-%m-%d"),
                    date_close=datetime.strptime(date_close, "%d.%m.%Y") if date_close else None,
                    trade_open=trade_open,
                    trade_close=float(trade_close) if trade_close else None,
                    net_income=float(net_income) if net_income else None,
                    count=count,
                    trade_type_id=type_options[trade_type],
                    trade_code_id=code_options[trade_code],
                    user_id=1,
                )
                await st.session_state.trade_repo.add(trade)
                st.success("Сделка добавлена!")
                st.rerun()


# ---------- Редактирование ----------
async def _edit_trade_form():
    with st.expander("✏️ Редактировать сделку"):
        trades = await st.session_state.trade_repo.get_all()
        if not trades:
            st.info("Нет сделок для редактирования.")
            return

        trade_dict = {f"{t.id} | {t.trade_code.exchange_id}": t.id for t in trades}
        selected_key = st.selectbox("Выберите сделку", list(trade_dict.keys()))
        selected_id = trade_dict[selected_key]
        trade = await st.session_state.trade_repo.get_by_id(selected_id)

        with st.form("edit_trade"):
            date_open = st.text_input("DateOpen", trade.date_open.strftime("%Y-%m-%d"))
            date_close = st.text_input("DateClose", trade.date_close.strftime("%Y-%m-%d") if trade.date_close else "")
            trade_open = st.number_input("TradeOpen", value=trade.trade_open)
            trade_close = st.text_input("TradeClose", str(trade.trade_close or ""))
            net_income = st.text_input("NetIncome", str(trade.net_income or ""))
            count = st.number_input("Count", min_value=1, value=trade.count, step=1)
            trade_type_id = st.number_input("TradeType ID", min_value=1, value=trade.trade_type_id, step=1)
            trade_code_id = st.number_input("TradeCode ID", min_value=1, value=trade.trade_code_id, step=1)
            save_btn = st.form_submit_button("Сохранить изменения")

            if save_btn:
                await st.session_state.trade_repo.update(
                    trade.id,
                    date_open=datetime.strptime(date_open, "%Y-%m-%d"),
                    date_close=datetime.strptime(date_close, "%Y-%m-%d") if date_close else None,
                    trade_open=trade_open,
                    trade_close=float(trade_close) if trade_close else None,
                    net_income=float(net_income) if net_income else None,
                    count=count,
                    trade_type_id=trade_type_id,
                    trade_code_id=trade_code_id,
                )
                st.success("Изменения сохранены!")
                st.rerun()


# ---------- Удаление ----------
async def _delete_trade_form():
    with st.expander("🗑 Удалить сделку"):
        trades = await st.session_state.trade_repo.get_all()
        if not trades:
            st.info("Нет сделок для удаления.")
            return
        ids = [t.id for t in trades]
        selected_id = st.selectbox("Выбери ID", ids)
        if st.button("Удалить"):
            await st.session_state.trade_repo.delete(selected_id)
            st.success("Удалено!")
            st.rerun()
