from sqlalchemy import create_engine, ForeignKey, String, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

from .. import Base

class UserAnime(Base):
    __tablename__='users_and_anime'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    anime_id: Mapped[int] = mapped_column(ForeignKey('anime.id'))

    user: Mapped['User'] = relationship('User', back_populates='anime', foreign_keys=[user_id])
    anime: Mapped['Anime'] = relationship('Anime', back_populates='users', foreign_keys=[anime_id])