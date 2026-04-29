from fastapi import APIRouter
from app.schemas.tryout_schema import TryoutStartRequest, TryoutSubmitRequest
from app.services.tryout_service import (
    generate_adaptive_questions,
    calculate_score,
    predict_chance
)

router = APIRouter()

# 🚀 START TRYOUT
@router.post("/tryout/start")
def start_tryout(data: TryoutStartRequest):
    questions = generate_adaptive_questions(data.jurusan)

    return {
        "status": "success",
        "questions": questions
    }

# 🚀 SUBMIT TRYOUT
@router.post("/tryout/submit")
def submit_tryout(data: TryoutSubmitRequest):
    score = calculate_score(data.questions, data.answers)
    peluang = predict_chance(score, data.kampus)

    return {
        "status": "success",
        "score": score,
        "peluang": peluang
    }