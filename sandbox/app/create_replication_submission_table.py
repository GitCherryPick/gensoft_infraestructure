from app.model.base import Base
from app.database import engine
from app.model.replication_submissions import ReplicationSubmission

# Asegurarse de que el modelo está importado y registrado
print("Creando tabla replication_submissions...")
Base.metadata.create_all(bind=engine)
print("Tabla creada exitosamente.")
