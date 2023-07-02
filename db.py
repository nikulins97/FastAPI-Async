import asyncpg

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel


DATABASE_URL = "postgresql+asyncpg://postgres:qwerty123@localhost/questions"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)


# Инициализация асинхронного движка SQLAlchemy
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Создание асинхронной сессии
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
