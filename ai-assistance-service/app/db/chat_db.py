from sqlalchemy.orm import Session
from app.model.chat_interaction import ChatInteraction

def save_important_message(db: Session, user_id: int, content: str, question: str):
    """
    Save an important message to the database.
    """
    saved = ChatInteraction(
        student_id=user_id,
        message_from_chat=content,
        message_from_user=question
    )
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved