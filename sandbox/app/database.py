from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_HOST = os.getenv('CODE_DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('CODE_DB_NAME')
DB_USER = os.getenv('CODE_DB_USER')
DB_PASSWORD = os.getenv('CODE_DB_PASSWORD')

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()