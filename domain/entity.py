from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, Str128, Str512, CreatedAt, UpdatedAt


class User(BaseModel):
    login: Mapped[Str128] = mapped_column(unique=True, nullable=False)
    hash_password: Mapped[Str512]
    last_login_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    refresh_token: Mapped[Str512 | None]

    trades: Mapped[list["Trade"]] = relationship(back_populates="user")


class TradeType(BaseModel):
    name: Mapped[Str128] = mapped_column(unique=True, nullable=False)

    trades: Mapped[list["Trade"]] = relationship(back_populates="trade_type")


class TradeCode(BaseModel):
    exchange_id: Mapped[Str128] = mapped_column(unique=True, nullable=False)
    description: Mapped[Str512 | None]

    trades: Mapped[list["Trade"]] = relationship(back_populates="trade_code")


class Trade(BaseModel):
    date_open: Mapped[datetime]
    date_close: Mapped[datetime | None]
    trade_open: Mapped[float]
    trade_close: Mapped[float | None]
    net_income: Mapped[float | None]
    count: Mapped[int]

    trade_type_id: Mapped[int] = mapped_column(ForeignKey("tradetypes.id"))
    trade_code_id: Mapped[int] = mapped_column(ForeignKey("tradecodes.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    trade_type: Mapped["TradeType"] = relationship(back_populates="trades")
    trade_code: Mapped["TradeCode"] = relationship(back_populates="trades")
    user: Mapped["User"] = relationship(back_populates="trades")
