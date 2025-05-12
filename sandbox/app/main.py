from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import executor
from app.model.base import Base
from .database import engine

from app.api.submissions import router as submissions_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hi World from Sandbox!"}

app.include_router(executor.router, tags=["executor"])
app.include_router(submissions_router, tags=["submissions"])
