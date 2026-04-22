# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegister(BaseModel):
    nama_lengkap: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "nama_lengkap": "Budi Santoso",
                "email": "budi@gmail.com",
                "password": "password123"
            }
        }


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "budi@gmail.com",
                "password": "password123"
            }
        }


class UserResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None