import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.model.base import Base

from app.api import courses, modules, contents
from fastapi.staticfiles import StaticFiles

import seed

Base.metadata.create_all(bind=engine)

seed.seed_data()

app = FastAPI(
    title="Content Management API",
    description="API para gestionar cursos, módulos y contenidos educativos",
    version="1.0.0"
)

current_dir = os.path.dirname(os.path.abspath(__file__))
storage_path = os.path.join(current_dir, "..", "storage")
app.mount("/storage", StaticFiles(directory=storage_path), name="storage")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],                   
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Content Management microservice!"}

@app.get("/pai")
def paila():
    return 124

app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(modules.router, prefix="/modules", tags=["modules"])
app.include_router(contents.router, prefix="/contents", tags=["contents"])