from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="API Gateway", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Alive!"}

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "https://gensoft.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["ngrok-skip-browser-warning"]
)

app.include_router(router)
