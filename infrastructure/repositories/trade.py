from sqlalchemy.ext.asyncio import AsyncSession
from domain.entity import Trade
from infrastructure.repositories.base_repository import BaseRepository

class TradeRepository(BaseRepository[Trade]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Trade)
