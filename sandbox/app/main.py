from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import executor

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
    return {"message": "Hi World from Sandbox!"}

app.include_router(executor.router, tags=["executor"])
app.include_router(executor.router)
