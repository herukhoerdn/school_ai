from pydantic import BaseModel
from typing import List

class AssessmentRequest(BaseModel):
    answers: List[str]

class AssessmentResponse(BaseModel):
    jurusan: str