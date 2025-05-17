from sqlalchemy.orm import Session
from app.model.code_task import CodeTask
from app.schema.code_task import TaskRequest


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