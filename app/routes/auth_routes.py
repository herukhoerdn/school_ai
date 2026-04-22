# app/routes/auth_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user_schema import UserRegister, UserLogin, UserResponse
from app.services.auth_service import register_user, login_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_user(
        db,
        data.nama_lengkap,
        data.email,
        data.password
    )


@router.post("/login", response_model=UserResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(
        db,
        data.email,
        data.password
    )