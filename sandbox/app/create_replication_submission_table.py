from app.model.base import Base
from app.database import engine
from app.model.replication_submissions import ReplicationSubmission

Base.metadata.create_all(bind=engine)
