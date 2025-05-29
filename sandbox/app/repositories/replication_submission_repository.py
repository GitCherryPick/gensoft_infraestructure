from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union
import json
from fastapi.encoders import jsonable_encoder
from app.model.replication_submissions import ReplicationSubmission as DBReplicationSubmission
from app.schema.replication_submission import ReplicationSubmissionCreate, ReplicationSubmissionUpdate, ReplicationSubmissionOut

def _serialize_list_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    list_fields = ['errores_sintacticos', 'diferencias_detectadas', 'pistas_generadas']
    for field in list_fields:
        if field in data and data[field] is not None and not isinstance(data[field], str):
            data[field] = json.dumps(data[field], ensure_ascii=False)
    return data

class ReplicationSubmissionRepository:
    @staticmethod
    def create(db: Session, submission: ReplicationSubmissionCreate) -> Dict[str, Any]:
        submission_data = submission.dict()
        submission_data = _serialize_list_fields(submission_data)
        
        db_submission = DBReplicationSubmission(**submission_data)
        
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
        
        return ReplicationSubmissionRepository._to_dict(db_submission)
    
    @staticmethod
    def get_by_id(db: Session, submission_id: int) -> Optional[Dict[str, Any]]:
        db_submission = db.query(DBReplicationSubmission).filter(DBReplicationSubmission.id == submission_id).first()
        if not db_submission:
            return None
        return ReplicationSubmissionRepository._to_dict(db_submission)
    
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        submissions = db.query(DBReplicationSubmission).offset(skip).limit(limit).all()
        return [ReplicationSubmissionRepository._to_dict(sub) for sub in submissions]
    
    def get_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        submissions = db.query(DBReplicationSubmission).filter(DBReplicationSubmission.user_id == user_id).offset(skip).limit(limit).all()
        return [ReplicationSubmissionRepository._to_dict(sub) for sub in submissions]
    
    def get_by_exercise_id(db: Session, exercise_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        submissions = db.query(DBReplicationSubmission).filter(DBReplicationSubmission.exercise_id == exercise_id).offset(skip).limit(limit).all()
        return [ReplicationSubmissionRepository._to_dict(sub) for sub in submissions]
    
    @staticmethod
    def get_by_user_and_exercise(
        db: Session, user_id: int, exercise_id: int
    ) -> List[Dict[str, Any]]:
        submissions = (
            db.query(DBReplicationSubmission)
            .filter(
                DBReplicationSubmission.user_id == user_id,
                DBReplicationSubmission.exercise_id == exercise_id,
            )
            .order_by(DBReplicationSubmission.submission_date.desc())
            .all()
        )
        return [ReplicationSubmissionRepository._to_dict(sub) for sub in submissions]
    
    @staticmethod
    def update(
        db: Session, submission_id: int, submission: ReplicationSubmissionUpdate
    ) -> Optional[Dict[str, Any]]:
        db_submission = db.query(DBReplicationSubmission).filter(DBReplicationSubmission.id == submission_id).first()
        if not db_submission:
            return None
            
        update_data = submission.dict(exclude_unset=True)
        update_data = ReplicationSubmissionRepository._serialize_list_fields(update_data)
        
        for key, value in update_data.items():
            setattr(db_submission, key, value)
            
        db.commit()
        db.refresh(db_submission)
        return ReplicationSubmissionRepository._to_dict(db_submission)
    
    @staticmethod
    def _to_dict(submission: DBReplicationSubmission) -> Dict[str, Any]:
        result = {}
        for column in DBReplicationSubmission.__table__.columns:
            value = getattr(submission, column.name)
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            result[column.name] = value
        
        json_fields = ['errores_sintacticos', 'diferencias_detectadas', 'pistas_generadas']
        for field in json_fields:
            if field in result and isinstance(result[field], str):
                try:
                    result[field] = json.loads(result[field])
                except json.JSONDecodeError:
                    result[field] = []
        
        return result
    
    @staticmethod
    def delete(db: Session, submission_id: int) -> bool:
        db_submission = db.query(DBReplicationSubmission).filter(DBReplicationSubmission.id == submission_id).first()
        if db_submission:
            db.delete(db_submission)
            db.commit()
            return True
        return False
