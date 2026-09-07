import pytest
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.database import Base,get_db
from sqlalchemy import create_engine
from minio.deleteobjects import DeleteObject
from app.services.storage_services import init_storage, minio_client


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
   init_storage()
   yield
   Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
   app.dependency_overrides[get_db] = overridden_get_db
   with TestClient(app) as test_client:
      yield test_client
   app.dependency_overrides.clear() 

@pytest.fixture()
def test_user(client):
   payload ={
       "email": "tester@example.com",
       "password": "strongpassword123"
   }
   client.post("/api/v1/auth/signup", json=payload)

   return payload

@pytest.fixture(scope='session',autouse=True)
def setup_and_cleanup_test_minio():
   test_bucket = settings.MINIO_TEST_BUCKET_NAME

   if not minio_client.bucket_exists(test_bucket):
      minio_client.make_bucket(test_bucket)

   original_bucket = settings.MINIO_BUCKET_NAME
   settings.MINIO_BUCKET_NAME = test_bucket

   yield

   objects_to_delete = [
      DeleteObject(obj.object_name) 
      for obj in minio_client.list_objects(test_bucket, recursive=True)
      if obj.object_name is not None
   ]   

   if objects_to_delete:
      for error in minio_client.remove_objects(test_bucket, objects_to_delete):

       settings.MINIO_BUCKET_NAME = original_bucket
   
@pytest.fixture
def valid_pdf_bytes() -> bytes:
    pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
        b"xref\n0 4\n0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"trailer\n<< /Size 4 /Root 1 0 R >>\n"
        b"startxref\n185\n%%EOF"
    )
    return pdf_content