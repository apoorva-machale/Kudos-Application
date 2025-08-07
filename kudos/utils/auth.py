from fastapi import Depends, HTTPException, Header, status
from sqlmodel import Session, select
from database import get_db, engine
from models.models import User
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from models.models import User, Organization, Role
import os
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    print(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
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
    #
    # Create default organization (if needed)
    org = session.exec(select(Organization).where(Organization.name == "DefaultOrg")).first()
    if not org:
        org = Organization(name="DefaultOrg")
        session.add(org)
        session.commit()
        session.refresh(org)

    # Create the admin user
    admin_user = User(
        username="admin",
        password="admin123", 
        email="admin@kudosapp.com",
        role=Role.admin
    )
    session.add(admin_user)
    session.commit()
