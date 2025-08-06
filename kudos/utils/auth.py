from fastapi import Depends, HTTPException, Header
from sqlmodel import Session
from database import get_db
from models.models import User


def get_current_user(x_user_id: int = Header(...), session: Session = Depends(get_db)) -> User:
    user = session.get(User, x_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
