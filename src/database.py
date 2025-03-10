from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
import aioboto3

from src.config import settings

DATABASE_URL = settings.db_url

Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(DATABASE_URL)
sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session


async def get_s3_client():
    session = aioboto3.Session()
    async with session.client(
        settings.s3_service_name,
        endpoint_url=settings.s3_url,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
    ) as s3_client:
        yield s3_client
