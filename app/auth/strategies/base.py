from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class AuthStrategy(ABC):

    @abstractmethod
    async def authenticate(self, db: AsyncSession, data) -> User:
        ...
