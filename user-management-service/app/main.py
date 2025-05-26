from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.model.base import Base

from app.api import institutions
from app.api import auth 
from app.api import user
from app.api import grade
from app.api import student_transfer
from app.api import feedback_tasks
from app.api.reset_password import router as reset_password_router

import sys
import os


# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to User Management microservice!"}

app.include_router(institutions.router)
app.include_router(reset_password_router, prefix="/auth", tags=["auth"])
app.include_router(auth.router, tags=["auth"])
app.include_router(user.router, tags=["users"])
app.include_router(grade.router, tags=["grades"])
app.include_router(student_transfer.router, tags=["student_transfers"])
app.include_router(feedback_tasks.router, prefix="/feedback", tags=["feedback"])