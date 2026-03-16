import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.main import app
from backend.app.db import Base, get_db

# Setup database khusus untuk testing (QA Best Practice)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_notes_pagination_and_sorting():
    # 1. Buat beberapa catatan dummy
    titles = ["Alpha", "Gamma", "Beta"]
    for t in titles:
        res = client.post("/notes/", json={"title": t, "content": "Test content"})
        # QA Check: Pastikan post berhasil
        assert res.status_code == 201 

    # Tambahkan jeda sinkronisasi kecil jika perlu, atau langsung ambil
    response = client.get("/notes/?sort=title")
    data = response.json()
    
    # Debugging: Cetak data jika gagal lagi (opsional)
    # print(data) 
    
    assert response.status_code == 200
    assert len(data) >= 3 # Pastikan minimal ada 3 data
    assert data[0]["title"] == "Alpha"