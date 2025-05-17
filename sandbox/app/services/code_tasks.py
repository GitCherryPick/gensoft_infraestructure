from sqlalchemy.orm import Session
from app.model.code_task import CodeTask
from app.schema.code_task import TaskRequest, StudentReply


def get_code_task(db: Session, id: int):
    return db.query(CodeTask).filter(CodeTask.id == id).first()

def create_code_task(db: Session, task: TaskRequest):
    new_task = CodeTask(
        title=task.title,
        description=task.description,
        expected_code=task.expected_code,
        expected_result=task.expected_result,
        template_code=task.template_code,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_code_task(db: Session, id: int, task: TaskRequest):
    db_rep_task = get_code_task(db, id)
    if not db_rep_task:
        return None
    for field, value in task.dict(exclude_unset=True).items():
        setattr(db_rep_task, field, value)
    db.commit()
    db.refresh(db_rep_task)
    return db_rep_task


def delete_code_task(db: Session, id: int):
    db_rep_task = get_code_task(db, id)
    if db_rep_task:
        db.delete(db_rep_task)
        db.commit()
    return db_rep_task

def submit_code(db: Session, submission: StudentReply):
    task_replicator = db.query(CodeTask).filter(CodeTask.id == submission.task_replicator_id).first()
    if not task_replicator:
        return {"error": "Tarea de replicacion no encontrada"}
    
    if submission.student_code.strip() == task_replicator.expected_code.strip():
        return {"result": "Tarea completada con exito"}
    else:
        task_lines = task_replicator.expected_code.strip().splitlines()
        student_lines = submission.student_code.strip().splitlines()

        errors = []
        for i, (t_line, s_line) in enumerate(zip(task_lines, student_lines)):
            if t_line.strip() != s_line.strip():
                errors.append({
                    "line": i + 1,
                    "expected": t_line,
                    "got": s_line
                })

        if len(student_lines) != len(task_lines):
            errors.append({
                "message": "Hace falta que repliques correctamente",
                "expected_lines": len(task_lines),
                "got_lines": len(student_lines)
            })

        return {"result": "Incorrecto", "details": errors}

def get_template(db: Session, task_id: int):
    task = db.query(CodeTask).filter(CodeTask.id == task_id).first()

    if not task:
        return {"error": "Tarea no encontrada"}

    if task.template_code:
        return {"template_code": task.template_code}
    else:
        return {"message": "No hay plantilla, la tarea es de escritura completa."}