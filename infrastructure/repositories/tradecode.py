from sqlalchemy.ext.asyncio import AsyncSession
from domain.entity import TradeCode
from infrastructure.repositories.base_repository import BaseRepository

class TradeCodeRepository(BaseRepository[TradeCode]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TradeCode)
