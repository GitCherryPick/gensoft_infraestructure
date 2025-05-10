from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import student_stats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to AI Support microservice!"}

app.include_router(student_stats.router, tags=["student_stats"])