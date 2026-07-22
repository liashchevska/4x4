from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine("sqlite:///data.db")

Session = sessionmaker(bind=engine)


def get_session():
    with Session() as session:
        yield session
