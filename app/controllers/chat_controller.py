# app/controllers/chat_controller.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.chat_schema import ChatRequest, ChatResponse, RiwayatResponse
from app.services.ai_service import get_rekomendasi
from app.repositories.chat_repository import simpan_chat, ambil_riwayat_chat
from pydantic import BaseModel

router = APIRouter()


@router.post("/rekomendasi", response_model=ChatResponse)
def rekomendasi_jurusan(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    hasil = get_rekomendasi(request.pesan)

    return hasil


@router.get("/riwayat/{user_id}", response_model=RiwayatResponse)
def get_riwayat(user_id: int, db: Session = Depends(get_db)):
    riwayat = ambil_riwayat_chat(db, user_id)
    return {
        "status": "success",
        "data": riwayat
    }

class SimpanChatRequest(BaseModel):
    user_id: int
    pesan_user: str
    respons_ai: str

@router.post("/simpan")
def simpan_chat_endpoint(request: SimpanChatRequest, db: Session = Depends(get_db)):
    simpan_chat(db, request.user_id, request.pesan_user, request.respons_ai)
    return {"status": "success"}