from logging.config import fileConfig
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from domain.base import BaseModel
from domain.entity import User, TradeType, TradeCode, Trade

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Offline режим (без подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Запуск миграций."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Online режим (через асинхронный движок)."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        future=True,
        echo=False,
    )

    async with connectable.begin() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
