from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from app.model.exam import Exam
from app.model.exam_response import ExamResponse

from app.database import get_db
from app.schema.exam import ExamCreate, ExamOut
from app.schema.exam_response import ExamResponseCreate, ExamResponseOut

router = APIRouter(tags=["exams"])

@router.post("/exams", response_model=ExamOut, status_code=status.HTTP_201_CREATED)
def create_exam(exam: ExamCreate, db: Session = Depends(get_db)):
    db_exam = Exam(**exam.model_dump())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam

@router.get("/exams/last", response_model=ExamOut, status_code=status.HTTP_200_OK)
def get_last_exam(db: Session = Depends(get_db)):
    db_exam = db.query(Exam).order_by(Exam.exam_id.desc()).first()
    if not db_exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se creo ningun examen")
    return db_exam

@router.post("/grade/exam", response_model=ExamResponseOut)
def submit_exam(responses: ExamResponseCreate, db: Session = Depends(get_db)):
    # 1. Obtener el examen
    db_exam = db.query(Exam).filter(Exam.exam_id == responses.exam_id).first()
    if not db_exam:
        raise HTTPException(status_code=404, detail="No existe un examen relacionado con ")
    db_response = ExamResponse(**responses.model_dump())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response
