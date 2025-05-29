from sqlalchemy import inspect
from app.database import engine
from app.model.base import Base
import logging

# Importamos el modelo explícitamente para asegurar que esté registrado
from app.model.replication_submissions import ReplicationSubmission

def initialize_database():
    logging.info("Inicializando base de datos...")
    inspector = inspect(engine)
    
    # Verificar si la tabla ya existe
    if not inspector.has_table('replication_submissions'):
        logging.info("Creando tabla 'replication_submissions'...")
        # Crear SOLO la tabla replication_submissions
        ReplicationSubmission.__table__.create(engine)
        logging.info("Tabla 'replication_submissions' creada exitosamente")
    else:
        logging.info("La tabla 'replication_submissions' ya existe")
        
    logging.info("Inicialización de base de datos completa")

if __name__ == "__main__":
    initialize_database()
