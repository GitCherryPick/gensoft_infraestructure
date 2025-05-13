from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "reset-secret"  # preferiblemente usar os.getenv
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except:
        return None
