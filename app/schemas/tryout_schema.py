from pydantic import BaseModel
from typing import List


class TryoutStartRequest(BaseModel):
    jurusan: str
    kampus: List[str]


class QuestionSchema(BaseModel):
    question: str
    options: List[str]
    correct_answer: str


class TryoutSubmitRequest(BaseModel):
    user_answers: List[str]
    questions: List[QuestionSchema]
    kampus: List[str]