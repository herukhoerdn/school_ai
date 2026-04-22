# app/models/chat.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base


class Chat(Base):
    __tablename__ = "chats"

    # Primary key
    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Relasi ke tabel users
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Isi percakapan
    pesan_user = Column(Text, nullable=False)   # cerita/input dari siswa
    respons_ai = Column(Text, nullable=True)    # jawaban dari Gemini

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi ORM — bisa akses user dari objek chat
    user = relationship("User", back_populates="chats")

    def __repr__(self):
        return f"<Chat id={self.id} user_id={self.user_id}>"