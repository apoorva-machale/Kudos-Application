from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime


# ------------------------
# User Schemas
# ------------------------

class UserBase(BaseModel):
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=32, 
        pattern="^[A-Za-z0-9_]+$", 
        strip_whitespace=True
    )
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(...,min_length=8, max_length=128)
    org_id: int

    @field_validator('password')
    def validate_password(cls, value):
        if not any(c.isdigit() for c in value):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isalpha() for c in value):
            raise ValueError('Password must contain at least one letter')
        return value


class UserRead(UserBase):
    id: int
    org_id: int
    kudos_remaining: int

    class Config:
        orm_mode = True


# ------------------------
# Organization Schemas
# ------------------------

class OrganizationBase(BaseModel):
    name: str


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------
# Kudos Schemas
# ------------------------

class KudosBase(BaseModel):
    message: Optional[str] = None


class KudosCreate(KudosBase):
    receiver_id: int


class KudosRead(KudosBase):
    id: int
    giver_id: int
    receiver_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ------------------------
# Response Schemas
# ------------------------

class KudosReceived(KudosRead):
    giver: UserRead


class KudosGiven(KudosRead):
    receiver: UserRead