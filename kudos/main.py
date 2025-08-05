from fastapi import FastAPI, Depends, HTTPException
from kudos.database import engine, get_db
from .schemas.schemas import KudosCreate, UserCreate, OrganizationCreate
from .models import models
from .models.models import User, Kudos, Organization
from .crud.crud import give_kudos
from .utils.generate_demo_data import generate_demo_data
from .utils.auth import get_current_user
from .utils.scheduler import start_scheduler
from sqlmodel import SQLModel, Session


SQLModel.metadata.create_all(engine)
start_scheduler()

app = FastAPI()

@app.post("/generate-demo-data")
def generate_data(session: Session = Depends(get_db)):
    generate_demo_data(session)
    return {"message": "Demo data generated successfully!"}

@app.post("/organizations/")
def create_org(org: OrganizationCreate, session: Session = Depends(get_db)):
    organization = Organization(name=org.name)
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization

@app.post("/users/")
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    db_user = User(username=user.username, organization_id=user.org_id)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.post("/kudos/")
def give_kudos_api(
    kudos_data: KudosCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    try:
        kudos = give_kudos(session, current_user.id, kudos_data.receiver_id, kudos_data.message)
        return kudos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/me/kudos/received")
def get_my_kudos(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    return current_user.received_kudos


@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
