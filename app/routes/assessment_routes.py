from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.assessment_schema import AssessmentRequest
from app.services.assessment_service import analyze_and_parse
from app.models.assessment import Assessment
import json

router = APIRouter()


@router.post("/assessment")
def run_assessment(data: AssessmentRequest, db: Session = Depends(get_db)):
    # 🔹 Jalankan AI + parsing
    result = analyze_and_parse(data.answers)

    # 🔹 Simpan ke database
    new_data = Assessment(
        user_id=1,  # nanti bisa ambil dari login session
        answers=json.dumps(data.answers),
        result=json.dumps(result)
    )

    db.add(new_data)
    db.commit()

    # 🔹 Return ke frontend
    return {
        "status": "success",
        "data": result
    }

@router.get("/assessment/riwayat/{user_id}")
def get_riwayat(user_id: int, db: Session = Depends(get_db)):
    data = (
        db.query(Assessment)
        .filter(Assessment.user_id == user_id)
        .order_by(Assessment.id.desc())
        .all()
    )

    hasil = []
    for item in data:
        hasil.append({
            "id": item.id,
            "answers": json.loads(item.answers),
            "result": json.loads(item.result)
        })

    return {
        "status": "success",
        "data": hasil
    }