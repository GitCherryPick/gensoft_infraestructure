from fastapi import FastAPI
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.api import student_stats, api_ai
from app.model.base import Base
import app.model

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
    return {"message": "Welcome to AI Support microservice!"}

app.include_router(student_stats.router, prefix="/student-stats", tags=["Student Stats"])
app.include_router(api_ai.router, prefix="/ai", tags=["Gemini AI"])