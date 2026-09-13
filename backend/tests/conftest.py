import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.database import Base, get_session
from app.main import app
from app.models import Puzzle
from fastapi.testclient import TestClient
from factories import PUZZLE_PAYLOAD_VALID


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection, expire_on_commit=False)
    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(engine):
    def override_get_session():
        with Session(bind=engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def puzzle(session):
    puzzle = Puzzle.create(session, group_list=PUZZLE_PAYLOAD_VALID["groups"])
    session.commit()
    return puzzle
