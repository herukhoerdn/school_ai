from pydantic import BaseModel
from typing import List

class TryoutStartRequest(BaseModel):
    jurusan: str
    kampus: List[str]

class TryoutSubmitRequest(BaseModel):
    questions: list
    answers: List[str]
    kampus: List[str]