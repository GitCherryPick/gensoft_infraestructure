from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schema.code_task import TaskRequest, TaskResponse, StudentReply
from app.model.code_task import CodeTask
from app.services import code_tasks as replicator

router = APIRouter()

@router.post("/taskcode/", response_model= TaskResponse)
def create_task(task: TaskRequest, db: Session = Depends(get_db)):
    return replicator.create_code_task(db, task)

@router.get("/taskcode/", response_model=List[TaskResponse])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        tasks_all = db.query(CodeTask).offset(skip).limit(limit).all()
        return tasks_all
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener contenidos: {str(e)}")

@router.get("/taskcode/{id}", response_model=TaskResponse)
def read(id: int, db: Session = Depends(get_db)):
    task = replicator.get_code_task(db, id)
    if not task:
        raise HTTPException(status_code=404, detail="No se encuentra la tarea con ese id")
    return task

@router.put("/taskcode/{id}", response_model=TaskResponse)
def update(id: int, task: TaskRequest, db: Session = Depends(get_db)):
    updated = replicator.update_code_task(db, id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="No se puede actualizar la tarea con ese id")
    return updated

@router.delete("/taskcode/{id}", response_model=TaskResponse)
def delete(id: int, db: Session = Depends(get_db)):
    deleted = replicator.delete_code_task(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="No se puede eliminar la tarea con ese id")
    return deleted

@router.post("/codereplicated/")
def submit_code(submission: StudentReply, db: Session = Depends(get_db)):
    task_answer = replicator.submit_code(db, submission)
    if not task_answer:
        raise HTTPException(status_code=404, detail="No se puede enviar la tarea")
    return task_answer

@router.get("/taskcode/{id}/template")
def get_template(id: int, db: Session = Depends(get_db)):
    task = replicator.get_template(db, id)
    if not task:
        raise HTTPException(status_code=404, detail="No se encuentra la tarea con el id")
    return task