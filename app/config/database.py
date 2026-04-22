# app/config/database.py

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load file .env
load_dotenv()

# Ambil URL database dari .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Validasi — kalau .env belum diisi, langsung error yang jelas
if not DATABASE_URL:
    raise ValueError("DATABASE_URL belum diset di file .env")

# Engine — ini yang benar-benar terhubung ke PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,    # otomatis cek koneksi sebelum dipakai
    pool_size=5,           # jumlah koneksi yang disimpan
    max_overflow=10,       # koneksi tambahan kalau pool penuh
    echo=False             # ganti True kalau mau lihat query SQL di terminal
)

# Session factory — dipakai tiap kali ada request masuk
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base — semua model ORM akan inherit dari sini
Base = declarative_base()


def get_db():
    """
    Dependency injection untuk FastAPI.
    Dipanggil otomatis di setiap endpoint yang butuh database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection():
    """
    Test koneksi ke PostgreSQL.
    Panggil sekali saat server pertama kali jalan.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()
            print(f"[DB] Terhubung ke PostgreSQL: {version[0]}")
            return True
    except Exception as e:
        print(f"[DB] Gagal terhubung: {e}")
        return False