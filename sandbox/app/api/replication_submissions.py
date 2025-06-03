from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.database import get_db
from app.schema.replication_submission import (
    ReplicationSubmissionCreate,
    ReplicationSubmissionUpdate,
    ReplicationSubmissionOut,
)
from app.repositories.replication_submission_repository import ReplicationSubmissionRepository

router = APIRouter(prefix="/replication-submissions", tags=["replication-submissions"])

@router.post("/", response_model=ReplicationSubmissionOut, status_code=status.HTTP_201_CREATED)
def create_replication_submission(
    submission: ReplicationSubmissionCreate, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    try:
        result = ReplicationSubmissionRepository.create(db, submission)
        if not result:
            raise HTTPException(status_code=400, detail="Error al crear la entrega")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ReplicationSubmissionOut])
def get_all_replication_submissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ReplicationSubmissionRepository.get_all(db, skip, limit)

@router.get("/{submission_id}", response_model=ReplicationSubmissionOut)
def read_replication_submission(submission_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    submission = ReplicationSubmissionRepository.get_by_id(db, submission_id=submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return submission

@router.get("/user/{user_id}", response_model=List[ReplicationSubmissionOut])
def get_replication_submissions_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ReplicationSubmissionRepository.get_by_user_id(db, user_id, skip, limit)

@router.get("/user/{user_id}/exercise/{exercise_id}", response_model=List[ReplicationSubmissionOut])
def read_replication_submissions_by_user_and_exercise(
    user_id: int, exercise_id: int, db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    submissions = ReplicationSubmissionRepository.get_by_user_and_exercise(db, user_id=user_id, exercise_id=exercise_id)
    return submissions or []

@router.put("/{submission_id}", response_model=ReplicationSubmissionOut)
def update_replication_submission(
    submission_id: int, submission: ReplicationSubmissionUpdate, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    try:
        updated_submission = ReplicationSubmissionRepository.update(db, submission_id=submission_id, submission=submission)
        if not updated_submission:
            raise HTTPException(status_code=404, detail="Entrega no encontrada")
        return updated_submission
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_replication_submission(submission_id: int, db: Session = Depends(get_db)):
    deleted = ReplicationSubmissionRepository.delete(db, submission_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return {"message": "Entrega eliminada correctamente"}
    return {"message": "Replication submission deleted successfully"}
