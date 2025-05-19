import pytest
from tests.test_database import TestingSessionLocal, Base, engine
from app.main import app
from app.database import get_db
from fastapi.testclient import TestClient 
import app.model

@pytest.fixture(scope="function")
def db():
    print(f"Registered tables: {Base.metadata.tables.keys()}")  # Depuración
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

