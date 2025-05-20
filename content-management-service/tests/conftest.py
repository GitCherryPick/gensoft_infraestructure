import pytest
from sqlalchemy.orm import Session
from tests.test_database import TestingSessionLocal, Base, engine
from app import model # importa tus modelos reales

@pytest.fixture(scope="session")
def db():
    # Limpia todo y recrea tablas antes de correr tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

