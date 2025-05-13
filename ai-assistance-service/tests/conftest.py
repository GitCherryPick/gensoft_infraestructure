import pytest
from sqlalchemy.orm import Session
from tests.test_database import TestingSessionLocal, Base, engine
import app.model 

@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

