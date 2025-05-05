from fastapi import FastAPI
from app.database import engine
from app.model.base import Base
# Importar todos los modelos para que SQLAlchemy los registre
from app.model.courses import Course
from app.model.modules import Module
from app.model.contents import Content
from app.model.help_resource import HelpResource

# Importar routers
from app.api import courses, modules, contents

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Content Management API",
    description="API para gestionar cursos, módulos y contenidos educativos",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome OER Microservice here!"}

# Incluir routers
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(modules.router, prefix="/modules", tags=["modules"])
app.include_router(contents.router, prefix="/contents", tags=["contents"])
