from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime
import os
import uuid
import shutil

from app.database import SessionLocal
from app.model.content import Content
from app.model.module import Module
from app.schema.contents import ContentCreate, ContentOut, ContentUpdate, TextContentCreate, UrlContentCreate

router = APIRouter()

UPLOAD_DIR = "storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "pdf"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "videos"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "slides"), exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_module_exists(module_id: int, db: Session):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail=f"Módulo con ID {module_id} no encontrado")
    return module

# CRUD básico para contenidos
@router.post("/", response_model=ContentOut, status_code=status.HTTP_201_CREATED)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo contenido (sin archivo)
    """
    try:
        # Verificar que el módulo existe
        verify_module_exists(content.module_id, db)
        
        db_content = Content(
            module_id=content.module_id,
            content_type=content.content_type,
            title=content.title,
            content=content.content,
            video_url=content.video_url,
            file_path=content.file_path,
            created_at=datetime.now()
        )
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear contenido: {str(e)}")

@router.get("/", response_model=List[ContentOut])
def get_contents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de contenidos
    """
    try:
        contents = db.query(Content).offset(skip).limit(limit).all()
        return contents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener contenidos: {str(e)}")

@router.get("/module/{module_id}", response_model=List[ContentOut])
def get_contents_by_module(module_id: int, db: Session = Depends(get_db)):
    """
    Obtener contenidos por módulo
    """
    try:
        # Verificar que el módulo existe
        verify_module_exists(module_id, db)
        
        contents = db.query(Content).filter(Content.module_id == module_id).all()
        return contents
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener contenidos: {str(e)}")

@router.get("/module/{module_id}/type/{content_type}", response_model=List[ContentOut])
def get_contents_by_module_and_type(module_id: int, content_type: str, db: Session = Depends(get_db)):
    """
    Obtener contenidos por módulo y tipo
    """
    try:
        verify_module_exists(module_id, db)
        valid_types = ["text", "pdf", "image", "video", "slide", "url"]
        if content_type not in valid_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de contenido no válido. Tipos válidos: {', '.join(valid_types)}"
            )
        
        contents = db.query(Content).filter(
            Content.module_id == module_id,
            Content.content_type == content_type
        ).all()
        return contents
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener contenidos: {str(e)}")

@router.get("/{content_id}", response_model=ContentOut)
def get_content(content_id: int, db: Session = Depends(get_db)):
    """
    Obtener un contenido específico
    """
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        if content is None:
            raise HTTPException(status_code=404, detail="Contenido no encontrado")
        return content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener contenido: {str(e)}")

@router.put("/{content_id}", response_model=ContentOut)
def update_content(content_id: int, content_update: ContentUpdate, db: Session = Depends(get_db)):
    """
    Actualizar un contenido existente
    """
    try:
        db_content = db.query(Content).filter(Content.id == content_id).first()
        if db_content is None:
            raise HTTPException(status_code=404, detail="Contenido no encontrado")
        
        update_data = content_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_content, field, value)
        
        db.commit()
        db.refresh(db_content)
        return db_content
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar contenido: {str(e)}")

@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content(content_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un contenido
    """
    try:
        db_content = db.query(Content).filter(Content.id == content_id).first()
        if db_content is None:
            raise HTTPException(status_code=404, detail="Contenido no encontrado")
        
        if db_content.file_path and os.path.exists(db_content.file_path):
            os.remove(db_content.file_path)
        
        db.delete(db_content)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar contenido: {str(e)}")


@router.post("/text", response_model=ContentOut)
def create_text_content(content_data: TextContentCreate, db: Session = Depends(get_db)):
    """
    Crear contenido de tipo texto
    """
    try:
        verify_module_exists(content_data.module_id, db)
        
        db_content = Content(
            module_id=content_data.module_id,
            content_type="text",
            title=content_data.title,
            content=content_data.content,
            created_at=datetime.now()
        )
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear contenido de texto: {str(e)}")

@router.post("/url", response_model=ContentOut)
def create_url_content(content_data: UrlContentCreate, db: Session = Depends(get_db)):
    """
    Crear contenido de tipo URL
    """
    try:
        verify_module_exists(content_data.module_id, db)
        
        db_content = Content(
            module_id=content_data.module_id,
            content_type="url",
            title=content_data.title,
            video_url=content_data.url,
            created_at=datetime.now()
        )
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear contenido de URL: {str(e)}")

@router.get("/types", response_model=Dict[str, List[str]])
def get_content_types():
    """
    Obtener información sobre los tipos de contenido válidos
    """
    return {
        "valid_types": ["text", "pdf", "image", "video", "slide", "url"],
        "file_types": {
            "pdf": ["application/pdf"],
            "image": ["image/jpeg", "image/png", "image/gif", "image/webp"],
            "video": ["video/mp4", "video/webm", "video/mpeg"],
            "slide": [
                "application/vnd.ms-powerpoint",
                "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            ]
        }
    }
