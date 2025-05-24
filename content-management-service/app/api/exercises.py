from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.model.exercise import Exercise
from app.schema.exercise import ExerciseCreate, ExerciseOut

import json

router = APIRouter()

@router.post("/", response_model=ExerciseOut, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    exercise_data = exercise.model_dump()
    exercise_data["visible_lines"] = json.dumps(exercise_data["visible_lines"])
    db_exercise = Exercise(**exercise_data)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return ExerciseOut(
        exercise_id=db_exercise.exercise_id,
        instructor_id=db_exercise.instructor_id,
        title=db_exercise.title,
        prompt=db_exercise.prompt,
        target_code=db_exercise.target_code,
        visible_lines=exercise.visible_lines,
        instructor_comment=db_exercise.instructor_comment,
    )

@router.get("/", response_model=ExerciseOut)
def get_last_exercise(db: Session = Depends(get_db)):
    db_exercise = db.query(Exercise).order_by(Exercise.exercise_id.desc()).first()
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    visible_lines = json.loads(db_exercise.visible_lines)
    if db_exercise.visible_lines is None:
        db_exercise.visible_lines = []
    return ExerciseOut(
        exercise_id=db_exercise.exercise_id,
        instructor_id=db_exercise.instructor_id,
        title=db_exercise.title,
        prompt=db_exercise.prompt,
        target_code=db_exercise.target_code,
        visible_lines=visible_lines,
        instructor_comment=db_exercise.instructor_comment,
    )