# app/repositories/chat_repository.py

from sqlalchemy.orm import Session
from app.models.chat import Chat


def simpan_chat(db: Session, user_id: int, pesan_user: str, respons_ai: str):
    chat = Chat(
        user_id    = user_id,
        pesan_user = pesan_user,
        respons_ai = respons_ai
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def ambil_riwayat_chat(db: Session, user_id: int):
    return db.query(Chat)\
             .filter(Chat.user_id == user_id)\
             .order_by(Chat.created_at.asc())\
             .all()


def hapus_semua_chat(db: Session, user_id: int):
    db.query(Chat).filter(Chat.user_id == user_id).delete()
    db.commit()