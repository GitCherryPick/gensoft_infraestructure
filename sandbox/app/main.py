from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import executor
from app.api import tasks
from app.api import code_tasks
from app.database import engine
from app.model.base import Base
from app.api.submissions import router as submissions_router


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

@app.get("/")
def root():
    return {"message": "Hi World from Sandbox!"}

app.include_router(executor.router, tags=["executor"])
app.include_router(tasks.router, tags=["tasks"])
app.include_router(submissions_router, tags=["submissions"])
app.include_router(code_tasks.router, tags=["code_replicator"])