from sqlalchemy import create_engine, ForeignKey, String, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine

engine = create_async_engine(
    url='sqlite+aiosqlite:///mydatabase.db',
    echo=True
)

Session = async_sessionmaker(bind=engine)

async def up(async_engine: AsyncEngine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop(async_engine: AsyncEngine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

class Base(DeclarativeBase):
    pass

from .models import(
    User,
    UserAnime,
    Anime
)
