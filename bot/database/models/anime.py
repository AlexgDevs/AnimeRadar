from sqlalchemy import create_engine, ForeignKey, String, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

from .. import Base

class Anime(Base):
    __tablename__='anime'

    id: Mapped[int] = mapped_column(primary_key=True)
    mal_id: Mapped[int]
    title: Mapped[str]
    photo_url: Mapped[str]
    last_episode: Mapped[str]
    synopsis: Mapped[str]

    users: Mapped[list['UserAnime']] = relationship('UserAnime', back_populates='anime')
