from sqlalchemy import Column, Integer, Text, ForeignKey
from app.config.database import Base

class Tryout(Base):
    __tablename__ = "tryouts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    jurusan = Column(Text)
    score = Column(Integer)
    result = Column(Text)  # JSON peluang