from sqlmodel import Session, select
from ..models.models import User, Kudos


def give_kudos(session: Session, giver_id: int, receiver_id: int, message: str):
    giver = session.get(User, giver_id)
    receiver = session.get(User, receiver_id)

    if giver is None or receiver is None:
        raise ValueError("User not found")

    if giver.organization_id != receiver.organization_id:
        raise ValueError("Users not in same organization")

    if giver.kudos_remaining <= 0:
        raise ValueError("No kudos left to give this week")

    kudos = Kudos(giver_id=giver_id, receiver_id=receiver_id, message=message)
    session.add(kudos)

    giver.kudos_remaining -= 1
    session.commit()
    session.refresh(kudos)

    return kudos


def reset_kudos_weekly(session: Session):
    users = session.exec(select(User)).all()
    for user in users:
        user.kudos_remaining = 3
    session.commit()
