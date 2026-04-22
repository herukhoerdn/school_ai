# app/routes/chat_routes.py

from fastapi import APIRouter
from app.controllers.chat_controller import router as chat_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat", tags=["Chat & Rekomendasi"])