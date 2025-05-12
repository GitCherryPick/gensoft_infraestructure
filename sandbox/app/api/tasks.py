from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.tasks import Tasks
from app.model.tests import Tests
from app.schema.task import TaskCreate, TaskUpdate, TestCreate, TestBase
from app.database import SessionLocal

router = APIRouter()

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Tasks(title=task.title, enunciado=task.enunciado)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    for test in task.tests:
        db_test = Tests(task_id=db_task.id, input=test.input, output=test.output)
        db.add(db_test)

    db.commit()
    return {"message": "Tarea creada con éxito", "task_id": db_task.id}

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Tasks).all()
    return tasks

@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {
        "id": task.id,
        "title": task.title,
        "enunciado": task.enunciado,
        "tests": [{"id": t.id, "input": t.input, "output": t.output} for t in task.tests]
    }

@router.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    task.title = task_update.title
    task.enunciado = task_update.enunciado
    db.commit()
    return {"message": "Tarea actualizada correctamente"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    db.delete(task)
    db.commit()
    return {"message": "Tarea eliminada correctamente"}

@router.post("/tasks/{task_id}/tests")
def add_test(task_id: int, test: TestCreate, db: Session = Depends(get_db)):
    # Verificar que la tarea exista
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Crear y guardar el nuevo test
    new_test = Tests(task_id=task_id, input=test.input, output=test.output)
    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    return {
        "message": "Test agregado exitosamente",
        "test_id": new_test.id
    }

@router.delete("/tests/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Tests).filter(Tests.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")

    db.delete(test)
    db.commit()
    return {"message": "Test eliminado correctamente"}
