from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from database import engine, get_db
from schemas.schemas import KudosCreate, UserCreate, OrganizationCreate, LoginRequest, Token
from models import models
from models.models import User, Kudos, Organization
from crud.crud import give_kudos
from utils.generate_demo_data import generate_demo_data
from utils.auth import get_current_user, get_admin_user, create_access_token
from utils.scheduler import start_scheduler
from sqlmodel import SQLModel, Session, select
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from starlette.middleware.cors import CORSMiddleware

router = APIRouter(
    tags=['Kudos Application']
)

@router.post("/generate-demo-data")
def generate_data(session: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    generate_demo_data(session)
    return {"message": "Demo data generated successfully!"}

@router.post("/organizations/")
def create_org(org: OrganizationCreate, session: Session = Depends(get_db)):
    existing = session.exec(select(Organization).where(Organization.name == org.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization name already exists")

    organization = Organization(name=org.name)
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization

@router.post("/users/")
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    
    existing = session.exec(select(User).where(User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
        
    org = session.exec(select(Organization).where(Organization.name == user.org_name)).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    db_user = User(
        username=user.username,
        email=user.email,
        password=bcrypt.hash(user.password),
        organization_id=org.id,
        role="user"
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login_user(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = session.exec(select(User).where(User.username == data.username)).first()

    if not user or not bcrypt.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    org = session.get(Organization, user.organization_id)
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@router.post("/kudos/")
def give_kudos_api(
    kudos_data: KudosCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    # Check message content
    if not kudos_data.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    # Get receiver
    receiver = session.exec(
        select(User).where(User.username == kudos_data.receiver_username)
    ).first()

    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{kudos_data.receiver_username}' not found"
        )

    # Check if giving self kudos
    if receiver.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot give kudos to yourself"
        )

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while giving kudos."
        )



@router.get("/me/kudos/received")
def get_my_kudos(current_user: User = Depends(get_current_user)):
    return current_user.received_kudos


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "organization": current_user.organization.name,
        "role": current_user.role,
        "kudos_remaining": current_user.kudos_remaining
    }
