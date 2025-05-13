from sqlalchemy import create_engine
from app.database import Base
from sqlalchemy.orm import sessionmaker
import os
import app.model

DB_HOST = os.getenv('AI_DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('AI_DB_NAME_TEST') 
DB_USER = os.getenv('AI_DB_USER')
DB_PASSWORD = os.getenv('AI_DB_PASSWORD')

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"Using database: {SQLALCHEMY_DATABASE_URL}")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
