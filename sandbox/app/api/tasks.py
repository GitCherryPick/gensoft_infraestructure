from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.model.tasks import Tasks
from app.model.tests import Tests
from app.schema.task import TaskCreate, TaskUpdate, TestCreate, TaskOut
from app.database import SessionLocal
from app.schema.code_input import CodeInput2
from app.api.executor import execute_code
from app.model.submissions import Submission
from app.schema.submission import SubmissionInput 
from app.model.tests import Tests
from sandbox.app.services.submissions_user import generate_missing_submissions

from app.model.hints import Hints
from app.schema.hint import HintBase, HintCreate, HintUpdate, HintOut
from typing import Optional, List
from app.model.UsedHint import UsedHint
from sqlalchemy import func

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Endpoints para Hints ---
@router.post("/hints/", response_model=HintOut, status_code=status.HTTP_201_CREATED)
def create_new_hint(hint: HintCreate, db: Session = Depends(get_db)):
    if hint.task_id:
        task_exists = db.query(Tasks).filter(Tasks.id == hint.task_id).first()
        if not task_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {hint.task_id} not found. Cannot create hint for a non-existent task."
            )
            
    db_hint = Hints( 
        task_id=hint.task_id,
        hint_order=hint.hint_order,
        hint_text=hint.hint_text,
        penalty_points=hint.penalty_points
    )
    db.add(db_hint)
    db.commit()
    db.refresh(db_hint)
    return db_hint

@router.put("/hints/{hint_id}", response_model=HintOut)
def update_existing_hint(hint_id: int, hint_update: HintUpdate, db: Session = Depends(get_db)):
    db_hint = db.query(Hints).filter(Hints.hint_id == hint_id).first() # Using Hints directly
    if db_hint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hint not found")

    if hint_update.task_id is not None and hint_update.task_id != db_hint.task_id:
        task_exists = db.query(Tasks).filter(Tasks.id == hint_update.task_id).first()
        if not task_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cannot update hint: New task_id {hint_update.task_id} not found."
            )

    update_data = hint_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hint, key, value)
    
    db.add(db_hint)
    db.commit()
    db.refresh(db_hint)
    return db_hint

@router.get("/hints/{hint_id}", response_model=HintOut)
def get_hint(hint_id: int, db: Session = Depends(get_db)):
    db_hint = db.query(Hints).filter(Hints.hint_id == hint_id).first() # Using Hints directly
    if db_hint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hint not found")
    return db_hint

@router.get("/hints/", response_model=List[HintOut])
def get_all_hints(
    task_id: Optional[int] = Query(None, description="Filtra hints por ID de tarea"),
    skip: int = Query(0, description="Número de hints a omitir para paginación"),
    limit: int = Query(100, description="Número máximo de hints a devolver para paginación"),
    db: Session = Depends(get_db)
):
    query = db.query(Hints) # Using Hints directly
    if task_id is not None:
        query = query.filter(Hints.task_id == task_id) # Using Hints directly
    
    hints = query.offset(skip).limit(limit).all()
    return hints

@router.get("/hints/next")
def get_next_hint(user_id: int, task_id: int, db: Session = Depends(get_db)):
    used_hint_ids = db.query(UsedHint.hint_id).filter_by(
        user_id=user_id,
        task_id=task_id
    ).subquery()

    next_hint = db.query(Hints).filter(
        Hints.task_id == task_id,
        ~Hints.hint_id.in_(used_hint_ids)
    ).order_by(Hints.hint_order.asc()).first()

    if not next_hint:
        return {"message": "No hay más hints disponibles", "hint": None}

    return {
        "hint_id": next_hint.hint_id,
        "hint_text": next_hint.hint_text,
        "penalty_points": next_hint.penalty_points
    }


# --- Resto de tus Endpoints existentes (sin cambios) ---

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Tasks(**task.model_dump())
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


@router.get("/tasks/getScore")
def getScore(
    task_id: int = Query(..., title="ID de la tarea", example=1),
    user_id: int = Query(..., title="ID del usuario", example=1),
    db: Session = Depends(get_db)
):
    submissions = (
        db.query(Submission)
        .filter(
            Submission.user_id == user_id,
            Submission.task_id == task_id,
            Submission.tipo_problema == "tasks"
        )
        .all()
    )

    score = max((subi.score for subi in submissions), default=0)

    total_test_cases = db.query(Tests).filter(Tests.task_id == task_id).count()

    return {
        "score": score,
        "total_cases": total_test_cases
    }

@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_db = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task_db

@router.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    task.title = task_update.title
    task.enunciado = task_update.enunciado
    task.pistas = task_update.pistas
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
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

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


# logica de enviar

@router.post("/enviar")
def enviar(submission: SubmissionInput, db: Session = Depends(get_db)):
    # code_input_2_object = CodeInput2(code=submission.code, call="suma(1,2)")
    veredicts = []

    task_i = db.query(Tasks).filter(Tasks.id == submission.taskId).first()
    id = task_i.id

    test_cases = task_i.tests
    generalVeredict = "Accepted"
    countACs = 0

    for test_case in test_cases:
        result = execute_code(CodeInput2(code=submission.code, call=test_case.input))

        if result["error"]:
            veredict = "Error"
            error = result["error"]
        elif result["output"].rstrip('\n') == test_case.output.rstrip('\n'):
            countACs += 1
            veredict = "Accepted"
            error = ""
        else:
            veredict = "Wrong Answer"
            error = ""

        if veredict != "Accepted":
            generalVeredict = "Error"

        veredicts.append({
            "veredict": veredict,
            "error": error,
            "input": test_case.input,
            "expectedOutput": test_case.output.rstrip('\n'),
            "output": result["output"].rstrip('\n')
        })
    
    # Calcular penalización por hints
    penalidad_total = db.query(func.sum(Hints.penalty_points)).join(
        UsedHint, UsedHint.hint_id == Hints.hint_id
    ).filter(
        UsedHint.user_id == submission.UserId,
        UsedHint.task_id == submission.taskId
    ).scalar() or 0.0

    # Aquí puedes usar `menos` como penalización total
    menos = float(penalidad_total)
    nuevos_puntos = countACs - menos

    nueva_submission = Submission(
        user_id=submission.UserId,
        code=submission.code,
        result=generalVeredict,
        task_id=submission.taskId,
        tipo_problema="tasks",
        score=nuevos_puntos
    )


    db.add(nueva_submission)
    db.commit()

    return {
        "generalVeredict": generalVeredict,
        "testCases": veredicts
    }

@router.put("/task/{task_id}/close")
async def close_task(task_id:int, db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    if task.status == "Cerrada":
        return {"message": "La tarea ya está cerrada"}
    
    task.status = "Cerrada"
    db.commit()

    await generate_missing_submissions(task_id, db)

    return {"message": "Tarea cerrada y envíos generados para estudiantes sin envíos previos"}