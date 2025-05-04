from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal, engine
from app.model.base import Base
from app.model.courses import Course
from app.schema.course_schema import CourseOut

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome OER Microservice here!"}

@app.get("/courses", response_model=List[CourseOut])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de cursos
    """
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """
    Obtener un curso por su ID
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return course
