from fastapi import FastAPI, Depends, HTTPException
from database import engine
from schemas.schemas import KudosCreate, UserCreate, OrganizationCreate
from models import models
from models.models import User, Kudos, Organization
from crud.crud import give_kudos
from utils.generate_demo_data import generate_demo_data
from utils.auth import get_current_user
from utils.scheduler import start_scheduler
from sqlmodel import SQLModel, Session
from routers import routes
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import Session
from database import engine
from utils.auth import create_default_admin

SQLModel.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    start_scheduler()
    with Session(engine) as session:
        create_default_admin(session)
    yield 

app = FastAPI(lifespan=lifespan)
   
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routes.router)
