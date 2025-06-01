from sqlalchemy import inspect
from app.database import engine
from app.model.base import Base
import logging

from app.model.replication_submissions import ReplicationSubmission

def initialize_database():
    inspector = inspect(engine)
    
    if not inspector.has_table('replication_submissions'):
        ReplicationSubmission.__table__.create(engine)
    else:
        logging.info("La tabla 'replication_submissions' ya existe")
    
if __name__ == "__main__":
    initialize_database()
