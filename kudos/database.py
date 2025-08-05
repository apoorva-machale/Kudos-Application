from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL")
ALgorithm = os.getenv("ALGORITHM")
print("Hello",MYSQL_DATABASE_URL,ALgorithm)
engine = create_engine(MYSQL_DATABASE_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()