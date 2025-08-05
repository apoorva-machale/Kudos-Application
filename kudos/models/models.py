from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    users: List["User"] = Relationship(back_populates="organization")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    organization_id: int = Field(foreign_key="organization.id")
    kudos_remaining: int = 3
    organization: Organization = Relationship(back_populates="users")
    given_kudos: List["Kudos"] = Relationship(back_populates="giver", sa_relationship_kwargs={"foreign_keys": "[Kudos.giver_id]"})
    received_kudos: List["Kudos"] = Relationship(back_populates="receiver", sa_relationship_kwargs={"foreign_keys": "[Kudos.receiver_id]"})


class Kudos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    giver_id: int = Field(foreign_key="user.id")
    receiver_id: int = Field(foreign_key="user.id")
    message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    giver: User = Relationship(back_populates="given_kudos", sa_relationship_kwargs={"foreign_keys": "[Kudos.giver_id]"})
    receiver: User = Relationship(back_populates="received_kudos", sa_relationship_kwargs={"foreign_keys": "[Kudos.receiver_id]"})
