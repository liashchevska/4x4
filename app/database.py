from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.DATABASE_URL)

local_session = sessionmaker(bind=engine)


def get_session():
    with local_session() as session:
        yield session
