from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/dev.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base ini wajib ada untuk models.py
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        # Tambahkan ini di paling bawah file db.py
def apply_seed_if_needed():
    """
    Fungsi sementara agar tidak error saat diimpor oleh main.py.
    Nantinya bisa diisi logika untuk mengisi data awal database.
    """
    pass