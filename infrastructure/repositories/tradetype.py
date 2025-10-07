from sqlalchemy.ext.asyncio import AsyncSession
from domain.entity import TradeType
from infrastructure.repositories.base_repository import BaseRepository

class TradeTypeRepository(BaseRepository[TradeType]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TradeType)
