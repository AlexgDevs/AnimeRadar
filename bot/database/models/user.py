from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, String, MetaData, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

from .. import Base

class User(Base):
    __tablename__='users'

    id: Mapped[int] = mapped_column(primary_key=True)
    joined: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())

    anime: Mapped[list['UserAnime']] = relationship('UserAnime', back_populates='user')