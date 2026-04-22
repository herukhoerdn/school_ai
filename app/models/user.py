# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.config.database import Base
from sqlalchemy.orm import relationship 

class User(Base):
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Data utama
    nama_lengkap = Column(String(100), nullable=False)
    email        = Column(String(150), unique=True, index=True, nullable=False)
    password     = Column(String(255), nullable=False)  # disimpan dalam bentuk hash

    # Info siswa
    asal_sekolah = Column(String(200), nullable=True)
    kelas        = Column(String(20), nullable=True)  

    # Status akun
    is_active    = Column(Boolean, default=True)

    # Timestamp otomatis
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())

    chats = relationship("Chat", back_populates="user", cascade="all, delete")
    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"