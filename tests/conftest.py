import pytest
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.database import Base,get_db
from sqlalchemy import create_engine


engine = create_engine(settings.TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def overridden_get_db():
    db = TestingSessionLocal()
    try:
      yield db
    finally:
       db.close()  

@pytest.fixture(scope='session',autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)     

@pytest.fixture()
def client():
   app.dependency_overrides[get_db] = overridden_get_db
   with TestClient(app) as test_client:
      yield test_client
   app.dependency_overrides.clear()   
