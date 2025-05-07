from fastapi import FastAPI
from app.model.base import Base
from app.core.database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to Content Management microservice!"}

@app.get("/pai")
def paila():
    return 124
