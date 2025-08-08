from sqlmodel import Session, select
from models.models import User, Organization
from utils.http_exceptions import http_400, http_404

def validate_username_unique(session: Session, username: str):
    if session.exec(select(User).where(User.username == username)).first():
        raise http_400("Username already exists")

def validate_org_exists(session: Session, org_name: str) -> Organization:
    org = session.exec(select(Organization).where(Organization.name == org_name)).first()
    if not org:
        raise http_404("Organization not found")
    return org

def validate_not_self(current_user_id: int, receiver_id: int):
    if current_user_id == receiver_id:
        raise http_400("You cannot give kudos to yourself")

def validate_message_not_empty(message: str):
    if not message.strip():
        raise http_400("Message cannot be empty")
