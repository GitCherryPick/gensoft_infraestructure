from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="API Gateway", version="1.0.0")

origins = [
    "http://localhost",
    "http://localhost:3000",  # Cambia a la URL y puerto de tu frontend (ej. si es React, Vue, Angular)
    "http://localhost:8080",  # Añade otros puertos si tu frontend corre en varios
    # Si vas a desplegar tu aplicación en producción, aquí iría el dominio real de tu frontend
    # Por ejemplo: "https://tu-dominio-frontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Permite estas URLs de origen
    allow_credentials=True,         # Permite enviar cookies y encabezados de autenticación
    allow_methods=["*"],            # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],            # Permite todos los encabezados en las peticiones
)


app.include_router(router)