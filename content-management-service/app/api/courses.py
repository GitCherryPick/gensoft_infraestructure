from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime

from app.database import SessionLocal
from app.model.courses import Course
from app.schema.course import CourseOut, CourseCreate, CourseUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE - Crear un nuevo curso
@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo curso
    """
    try:
        db_course = Course(
            title=course.title,
            description=course.description,
            difficulty=course.difficulty,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear curso: {str(e)}")

# READ - Obtener todos los cursos
@router.get("/", response_model=List[CourseOut])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de cursos
    """
    try:
        courses = db.query(Course).offset(skip).limit(limit).all()
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener cursos: {str(e)}")

# READ - Obtener un curso específico por ID
@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """
    Obtener un curso por su ID
    """
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return course
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener curso: {str(e)}")

# UPDATE - Actualizar un curso existente
@router.put("/{course_id}", response_model=CourseOut)
def update_course(course_id: int, course_update: CourseUpdate, db: Session = Depends(get_db)):
    """
    Actualizar un curso existente
    """
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        update_data = course_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_course, field, value)
        db_course.updated_at = datetime.now()
        
        db.commit()
        db.refresh(db_course)
        return db_course
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar curso: {str(e)}")

# DELETE - Eliminar un curso
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un curso
    """
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        
        db.delete(db_course)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar curso: {str(e)}")

# Obtener ID del curso por defecto
@router.get("/default/id", response_model=Dict[str, int])
def get_default_course_id(db: Session = Depends(get_db)):
    """
    Obtener el ID del curso por defecto.
    Si no existe, lo crea y devuelve su ID.
    """
    try:
        default_title = "Introduccion a la programacion"
        
        default_course = db.query(Course).filter(Course.title == default_title).first()
        
        if default_course is None:
            default_course = Course(
                title=default_title,
                description="Curso introductorio a los fundamentos de la programación utilizando Python como lenguaje principal. Aprenderás conceptos básicos como variables, estructuras de control, funciones y más.",
                difficulty="facil",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(default_course)
            db.commit()
            db.refresh(default_course)
            
        return {"default_course_id": default_course.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener el curso por defecto: {str(e)}")
