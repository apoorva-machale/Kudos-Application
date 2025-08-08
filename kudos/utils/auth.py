from fastapi import Depends, HTTPException, Header, status
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from database import get_db, engine
from models.models import User, Kudos
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from models.models import User, Organization, Role
import os
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer
from config.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + settings.access_token_expires
    to_encode.update({"exp": expire})
    # Encode token using SECRET_KEY and ALGORITHM from settings
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode token and validate using SECRET_KEY and ALGORITHM
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    statement = (
        select(User)
        .options(
            selectinload(User.organization),  # eager-load organization
            selectinload(User.received_kudos).selectinload(Kudos.giver)  # eager-load kudos giver
        )
        .where(User.username == username)
    )

    user = session.exec(statement).first()

    if user is None:
        raise credentials_exception
    return user

def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Admin access only")
    return current_user


def create_default_admin(session: Session):
    # Check if an admin exists
    
    admin_exists = session.exec(
        select(User).where(User.role == Role.admin)
    ).first()

    if admin_exists:
        print("Admin user already exists. Skipping creation.")
        return

    # Create default organization (if needed)
    org = session.exec(select(Organization).where(Organization.name == "DefaultOrg")).first()
    if not org:
        org = Organization(name="DefaultOrg")
        session.add(org)
        session.flush() 

    # Create the admin user
    admin_user = User(
        username="admin",
        password=bcrypt.hash("Admin123"), 
        email="admin@kudosapp.com",
        role=Role.admin, 
        organization_id=org.id
    )
    session.add(admin_user)
    # Commit all changes to the database
    session.commit()

