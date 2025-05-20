from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import SessionLocal
from app.model.module import Module
from app.schema.module import ModuleOut, ModuleCreate, ModuleUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE - Crear un nuevo módulo
@router.post("/", response_model=ModuleOut, status_code=status.HTTP_201_CREATED)
def create_module(module: ModuleCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo módulo
    """
    try:
        db_module = Module(
            course_id=module.course_id,
            title=module.title,
            description=module.description,
            level=module.level,
            module_order=module.module_order
        )
        db.add(db_module)
        db.commit()
        db.refresh(db_module)
        return db_module
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear módulo: {str(e)}")

# READ - Obtener todos los módulos
@router.get("/", response_model=List[ModuleOut])
def get_modules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de módulos
    """
    try:
        modules = db.query(Module).offset(skip).limit(limit).all()
        return modules
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener módulos: {str(e)}")

# READ - Obtener módulos por curso
@router.get("/course/{course_id}", response_model=List[ModuleOut])
def get_modules_by_course(course_id: int, db: Session = Depends(get_db)):
    """
    Obtener módulos por curso
    """
    try:
        modules = db.query(Module).filter(Module.course_id == course_id).all()
        return modules
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener módulos: {str(e)}")

# READ - Obtener un módulo específico por ID
@router.get("/{module_id}", response_model=ModuleOut)
def get_module(module_id: int, db: Session = Depends(get_db)):
    """
    Obtener un módulo por su ID
    """
    try:
        module = db.query(Module).filter(Module.id == module_id).first()
        if module is None:
            raise HTTPException(status_code=404, detail="Module not found")
        return module
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener módulo: {str(e)}")

# UPDATE - Actualizar un módulo existente
@router.put("/{module_id}", response_model=ModuleOut)
def update_module(module_id: int, module_update: ModuleUpdate, db: Session = Depends(get_db)):
    """
    Actualizar un módulo existente
    """
    try:
        db_module = db.query(Module).filter(Module.id == module_id).first()
        if db_module is None:
            raise HTTPException(status_code=404, detail="Module not found")
        
        update_data = module_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_module, field, value)
        
        db.commit()
        db.refresh(db_module)
        return db_module
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar módulo: {str(e)}")

# DELETE - Eliminar un módulo
@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(module_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un módulo
    """
    try:
        db_module = db.query(Module).filter(Module.id == module_id).first()
        if db_module is None:
            raise HTTPException(status_code=404, detail="Module not found")
        
        db.delete(db_module)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar módulo: {str(e)}")
