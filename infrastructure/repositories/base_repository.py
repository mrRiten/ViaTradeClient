from typing import Type, Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from domain.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, obj_id: int) -> T | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def update(self, obj_id: int, **kwargs) -> T | None:
        await self.session.execute(
            update(self.model).where(self.model.id == obj_id).values(**kwargs)
        )
        await self.session.commit()
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, obj_id: int) -> None:
        await self.session.execute(
            delete(self.model).where(self.model.id == obj_id)
        )
        await self.session.commit()
