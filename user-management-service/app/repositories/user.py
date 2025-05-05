from sqlalchemy.orm import Session
from ..model.users import User  
from ..core.security import get_password_hash

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def update_user_password(email: str, new_password: str, db: Session):
    user = get_user_by_email(email, db)
    if not user:
        return False
    hashed_password = get_password_hash(new_password)
    user.password_hash = hashed_password
    db.commit()
    db.refresh(user)
    return True
