from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.model import StudentTransfer
from app.schema.student_transfers import StudentTransferCreate, StudentTransferResponse
from app.database import get_db

router = APIRouter(prefix="/student_transfers", tags=["student_transfers"])

@router.post("/", response_model=StudentTransferResponse)
def create_student_transfer(transfer: StudentTransferCreate, db: Session = Depends(get_db)):
    db_transfer = StudentTransfer(**transfer.model_dump())
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

@router.get("/{transfer_id}", response_model=StudentTransferResponse)
def get_student_transfer(transfer_id: int, db: Session = Depends(get_db)):
    transfer = db.query(StudentTransfer).filter(StudentTransfer.id == transfer_id).first()
    if transfer is None:
        return {"error": "student transfer not found"}
    return transfer