import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base

@pytest.fixture(scope='session')
def engine():
    engine = create_engine('sqlite+pysqlite:///:memory:')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope='function')
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    
    session = Session(bind=connection, expire_on_commit=False)
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()