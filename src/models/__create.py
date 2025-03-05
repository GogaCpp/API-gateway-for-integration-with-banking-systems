import asyncio

from .document import Document
from .contract import Contract
from .user_type import UserType
from .user import User

from ..database import Base, engine


if __name__ == "__main__":
    async def create_all() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(create_all())