from fastapi import FastAPI
from app.database import engine
from app.model.base import Base

from app.api import courses, modules, contents

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Content Management API",
    description="API para gestionar cursos, módulos y contenidos educativos",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to Content Management microservice!"}

@app.get("/pai")
def paila():
    return 124

# Incluir routers
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(modules.router, prefix="/modules", tags=["modules"])
app.include_router(contents.router, prefix="/contents", tags=["contents"])