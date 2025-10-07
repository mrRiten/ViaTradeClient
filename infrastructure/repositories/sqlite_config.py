from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

sqlite_url = URL.create(
    "sqlite+aiosqlite",
    database="local_db.sqlite3"
)

engine = create_async_engine(sqlite_url, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
