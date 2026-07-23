from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.DATABASE_URL)

Session = sessionmaker(bind=engine)


def get_session():
    with Session() as session:
        yield session
