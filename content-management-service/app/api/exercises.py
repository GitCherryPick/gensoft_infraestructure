from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.model.exercise import Exercise
from app.schema.exercise import ExerciseCreate, ExerciseOut

router = APIRouter()

@router.post("/", response_model=ExerciseOut, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    exercise_db = Exercise(**exercise.model_dump())
    db.add(exercise_db)
    db.commit()
    db.refresh(exercise_db)
    return exercise_db
