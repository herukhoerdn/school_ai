# app/schemas/chat_schema.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    pesan: str

    class Config:
        json_schema_extra = {
            "example": {
                "pesan": "Saya suka desain, main game, dan suka bikin konten YouTube"
            }
        }


class ChatResponse(BaseModel):
    status: str
    pesan: str
    rekomendasi: Optional[list] = None


class RiwayatItem(BaseModel):
    id: int
    pesan_user: str
    respons_ai: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RiwayatResponse(BaseModel):
    status: str
    data: List[RiwayatItem]