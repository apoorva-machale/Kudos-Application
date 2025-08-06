from sqlmodel import Session
from models.models import Organization, User, Kudos
import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker()

def get_random_past_datetime(weeks_back=8):
    """Return a random datetime in the past `weeks_back` weeks."""
    now = datetime.utcnow()
    start_date = now - timedelta(weeks=weeks_back)
    # Random time between start_date and now
    random_seconds = random.randint(0, int((now - start_date).total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

def generate_demo_data(session: Session):
    org_names = ["Alpha Org", "Beta Org", "Gamma Org"]
    messages = [
        "Great job!",
        "Amazing work!",
        "Thanks for helping!",
        "Well done!",
        "Incredible effort!",
    ]

    # Create organizations
    orgs = []
    for name in org_names:
        org = Organization(name=name)
        session.add(org)
        orgs.append(org)
    session.commit()

    # Create users in each organization
    users_by_org = {}
    for org in orgs:
        users = []
        for _ in range(random.randint(3, 5)):
            user = User(
                username=faker.user_name(),
                organization_id=org.id,
                kudos_remaining=3
            )
            session.add(user)
            users.append(user)
        users_by_org[org.id] = users
    session.commit()

    # Give kudos randomly across past N weeks and times
    for org_id, users in users_by_org.items():
        for giver in users:
            receivers = [u for u in users if u.id != giver.id]
            for _ in range(random.randint(1, 3)):
                if giver.kudos_remaining > 0 and receivers:
                    receiver = random.choice(receivers)
                    created_at = get_random_past_datetime(weeks_back=8)

                    kudos = Kudos(
                        giver_id=giver.id,
                        receiver_id=receiver.id,
                        message=random.choice(messages),
                        created_at=created_at
                    )
                    session.add(kudos)
                    giver.kudos_remaining -= 1
    session.commit()
