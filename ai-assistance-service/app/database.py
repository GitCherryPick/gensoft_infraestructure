from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('AI_DB_HOST', 'mysql-ai')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('AI_DB_NAME', 'ai_db')
DB_USER = os.getenv('AI_DB_USER', 'ai_user')
DB_PASSWORD = os.getenv('AI_DB_PASSWORD', 'ai_pass')

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()