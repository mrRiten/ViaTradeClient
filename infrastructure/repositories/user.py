from sqlalchemy.ext.asyncio import AsyncSession
from domain.entity import User
from infrastructure.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)
