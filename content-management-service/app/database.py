from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuración específica para Content Management (usa las variables de tu docker-compose.yml)
DB_HOST = os.getenv('DB_HOST', 'mysql-content')  # Nombre del servicio en Docker
DB_PORT = os.getenv('DB_PORT', '3306')          # Puerto interno del contenedor (no el mapeado 3308)
DB_NAME = os.getenv('DB_NAME', 'content_db')    # Nombre de la BD de contenido
DB_USER = os.getenv('DB_USER', 'content_user')  # Usuario específico para contenido
DB_PASSWORD = os.getenv('DB_PASSWORD', 'content_pass')  # Contraseña

# Cadena de conexión actualizada
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()