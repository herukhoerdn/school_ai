# app/models/jurusan.py

from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import ARRAY
from app.config.database import Base


class Jurusan(Base):
    __tablename__ = "jurusan"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Informasi utama jurusan
    nama        = Column(String(200), nullable=False, unique=True)
    fakultas    = Column(String(200), nullable=True)
    jenjang     = Column(String(10), nullable=False, default="S1")  # S1, D3, D4

    # Deskripsi jurusan
    deskripsi   = Column(Text, nullable=True)

    # Kata kunci minat — dipakai untuk matching dengan input siswa
    kata_kunci  = Column(ARRAY(String), nullable=False)
    # contoh: ["desain", "gambar", "visual", "seni", "kreatif"]

    # Prospek karir
    prospek_karir = Column(ARRAY(String), nullable=True)
    # contoh: ["UI/UX Designer", "Graphic Designer", "Art Director"]

    # Mata pelajaran yang relevan
    mapel_relevan = Column(ARRAY(String), nullable=True)
    # contoh: ["Seni Budaya", "TIK", "Matematika"]

    # Estimasi nilai rata-rata masuk (opsional, untuk info tambahan)
    passing_grade = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Jurusan id={self.id} nama={self.nama}>"