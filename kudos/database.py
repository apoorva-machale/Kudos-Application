from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MYSQL_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL")
print("MYSQL_DATABASE_URL", MYSQL_DATABASE_URL)

# Create the engine
engine = create_engine(MYSQL_DATABASE_URL, echo=True)

# Dependency for FastAPI routes
def get_db():
    with Session(engine) as session:
        yield session
