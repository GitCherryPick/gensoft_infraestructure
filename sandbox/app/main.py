from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import executor
from app.api import tasks
from app.api import code_tasks
from app.api import submissions
from app.api import ai_feedback_router
from app.api import replication_submissions
from app.database import engine
from app.model.base import Base
from app.seed import seed_task_replicators
from app.initialize_db import initialize_database

app = FastAPI()

Base.metadata.create_all(bind=engine)

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
    initialize_database()  # Asegura que la tabla replication_submissions exista
    seed_task_replicators()

@app.get("/")
def root():
    return {"message": "Hi World from Sandbox!"}

app.include_router(executor.router, tags=["executor"])
app.include_router(tasks.router, tags=["tasks"])
app.include_router(code_tasks.router, tags=["code_replicator"])
app.include_router(submissions.router, tags=["submissions"])
app.include_router(ai_feedback_router.router, tags=["ai-feedback"])
app.include_router(replication_submissions.router, tags=["replication-submissions"])