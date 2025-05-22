from sqlalchemy import create_engine, ForeignKey, String, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine(
    url='sqlite:///mydatabase.db',
    echo=True
)

Session = sessionmaker(bind=engine)

def up():
    Base.metadata.create_all(engine)

def drop():
    Base.metadata.drop_all(engine)

class Base(DeclarativeBase):
    pass

from .models import(
    User,
    UserAnime,
    Anime
)
