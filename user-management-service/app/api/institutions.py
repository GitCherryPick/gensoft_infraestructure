from app.core.database import SessionLocal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.model.institutions import Institution
from app.schema.institutions import InstitutionResponse, InstitutionCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/institutions", response_model=InstitutionResponse)
def create_institution(institution: InstitutionCreate, db: Session = Depends(get_db)):
    db_institution = Institution(
        name=institution.name,
        address=institution.address,
        contact_email=institution.contact_email,
        website=institution.website,
    )
    db.add(db_institution)
    db.commit()
    db.refresh(db_institution)
    return db_institution


@router.get("/institutions/{institution_id}", response_model=InstitutionResponse)
def get_institution(institution_id: int, db: Session = Depends(get_db)):
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if institution is None:
        return {"error": "institution not found"}
    return institution