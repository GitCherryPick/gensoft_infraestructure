from sqlalchemy.orm import Session
from app.model import StudentStats
from app.schema.student_stats import StudentStatsRequest,StudentStatsUpdateRequest, StudentStatsResponse

def get_student_stats(db: Session, student_id: int):
    """
    Get student stats by student ID.
    """
    return db.query(StudentStats).filter(StudentStats.student_id == student_id).first()

def create_student_stats(db: Session, stats: StudentStatsRequest):
    db_stats = StudentStats(**stats.dict())
    db.add(db_stats)
    db.commit()
    db.refresh(db_stats)
    return db_stats


def update_student_stats(db: Session, student_id: int, stats: StudentStatsUpdateRequest):
    db_stats = get_student_stats(db, student_id)
    if not db_stats:
        return None
    for field, value in stats.dict(exclude_unset=True).items():
        setattr(db_stats, field, value)
    db.commit()
    db.refresh(db_stats)
    return db_stats


def delete_student_stats(db: Session, student_id: int):
    db_stats = get_student_stats(db, student_id)
    if db_stats:
        db.delete(db_stats)
        db.commit()
    return db_stats