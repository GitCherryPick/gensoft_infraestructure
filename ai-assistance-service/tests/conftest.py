import pytest
from sqlalchemy.orm import Session
from tests.test_database import TestingSessionLocal, Base, engine
import app.model 

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

