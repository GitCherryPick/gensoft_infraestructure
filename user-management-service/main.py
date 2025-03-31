from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to User Management microservice!"}

@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = next(get_db())):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        return {"error": "Student not found"}
    return schemas.StudentResponse.from_orm(student)

@app.post("/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = next(get_db())):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return schemas.StudentResponse.from_orm(db_student)