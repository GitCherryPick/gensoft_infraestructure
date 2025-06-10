from sqlalchemy.orm import Session
from app.model.roles import Role
from app.database import SessionLocal

def seed_roles():
    db: Session = SessionLocal()

    if db.query(Role).first(): 
        print("Seed omitido.")
        db.close()
        return
    
    roles = [
        Role(
            name="estudiante",
            description="Puede enviar y resolver ejercicios de programacion" 
        ),
        Role(
            name="docente",
            description="Puede crear y revisar tareas de programacion" 
        )
    ]

    db.add_all(roles)
    db.commit()
    db.close()
    print("✅ Seed insertado de replicator con éxito")