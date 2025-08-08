from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from database import engine, get_db
from schemas.schemas import KudosCreate, UserCreate, OrganizationCreate, LoginRequest, Token
from models import models
from models.models import User, Kudos, Organization, Role
from crud.crud import give_kudos
from utils.generate_demo_data import generate_demo_data
from utils.auth import get_current_user, get_admin_user, create_access_token
from utils.scheduler import start_scheduler
from sqlmodel import SQLModel, Session, select
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from starlette.middleware.cors import CORSMiddleware
from utils.http_exceptions import http_401, http_500
from utils.validators import (
    validate_username_unique,
    validate_org_exists,
    validate_not_self,
    validate_message_not_empty
)

router = APIRouter(tags=['Kudos Application'])


# -------- DEMO DATA --------
@router.post("/generate-demo-data")
def generate_data(
    session: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    generate_demo_data(session)
    return {"message": "Demo data generated successfully!"}


# -------- ORGANIZATIONS --------
@router.post("/organizations/")
def create_org(org: OrganizationCreate, session: Session = Depends(get_db)):
    validate_username_unique(session, org.name)  # ensures unique name
    organization = Organization(name=org.name)
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization


# -------- USERS --------
@router.post("/users/")
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    validate_username_unique(session, user.username)
    org = validate_org_exists(session, user.org_name)

    db_user = User(
        username=user.username,
        email=user.email,
        password=bcrypt.hash(user.password),
        organization_id=org.id,
        role=Role.user
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# -------- LOGIN --------
@router.post("/login", response_model=Token)
def login_user(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db)
):
    user = session.exec(select(User).where(User.username == data.username)).first()
    if not user or not bcrypt.verify(data.password, user.password):
        raise http_401("Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# -------- GIVE KUDOS --------
@router.post("/kudos/")
def give_kudos_api(
    kudos_data: KudosCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    validate_message_not_empty(kudos_data.message)

    receiver = session.exec(
        select(User).where(User.username == kudos_data.receiver_username)
    ).first()
    if not receiver:
        raise http_401(f"User '{kudos_data.receiver_username}' not found")

    validate_not_self(current_user.id, receiver.id)

    try:
        kudos = give_kudos(
            session,
            current_user.id,
            receiver.id,
            kudos_data.message
        )
        return {
            "id": kudos.id,
            "message": kudos.message,
            "created_at": kudos.created_at,
            "giver_username": current_user.username,
            "receiver_username": receiver.username
        }
    except ValueError as e:
        raise http_401(str(e))
    except Exception:
        raise http_500("An unexpected error occurred while giving kudos.")


# -------- GET CURRENT USER --------
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "organization": current_user.organization.name,
        "role": current_user.role,
        "kudos_remaining": current_user.kudos_remaining,
        "received_kudos": [
            {
                "id": kudos.id,
                "message": kudos.message,
                "created_at": kudos.created_at,
                "giver_username": kudos.giver.username
            }
            for kudos in current_user.received_kudos
        ]
    }
