from sqlalchemy import Column, Integer, String, Text
from app.config.database import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    answers = Column(Text)   # simpan jawaban (json string)
    result = Column(Text)  # hasil jurusan