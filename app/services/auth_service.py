from sqlalchemy.orm import Session
from app.repositories.user_repository import get_user_by_email, create_user
from app.utils.hashing import hash_password, verify_password


def register_user(db: Session, nama_lengkap: str, email: str, password: str) -> dict:
    existing = get_user_by_email(db, email)
    if existing:
        return {
            "status": "error",
            "message": "Email sudah terdaftar"
        }

    hashed = hash_password(password)
    create_user(db, nama_lengkap, email, hashed)

    return {
        "status": "success",
        "message": "Pendaftaran berhasil"
    }


def login_user(db: Session, email: str, password: str) -> dict:
    user = get_user_by_email(db, email)
    if not user:
        return {
            "status": "error",
            "message": "Email tidak terdaftar"
        }

    if not verify_password(password, user.password):
        return {
            "status": "error",
            "message": "Password salah"
        }

    return {
         "status": "success",
        "message": f"Selamat datang, {user.nama_lengkap}!",
        "data": {                        
            "id": user.id,
            "nama_lengkap": user.nama_lengkap,
            "email": user.email
        }
    }