from sqlmodel import Session
from models.models import Organization, User, Kudos
import random
from datetime import datetime, timedelta
from faker import Faker
from passlib.hash import bcrypt

faker = Faker()

def get_random_past_datetime(weeks_back=8):
    now = datetime.utcnow()
    start_date = now - timedelta(weeks=weeks_back)
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

    #Create organizations (bulk)
    orgs = [Organization(name=name) for name in org_names]
    session.add_all(orgs)
    session.flush()  # Get IDs without committing yet

    #Create users for all orgs (bulk)
    users = []
    for org in orgs:
        for _ in range(random.randint(3, 5)):
            users.append(User(
                username=faker.user_name(),
                email=faker.email(),
                password=bcrypt.hash(faker.password()),  # Password hashed
                organization_id=org.id,
                kudos_remaining=3
            ))
    session.add_all(users)
    session.flush()  

    #Map users by org for kudos generation
    users_by_org = {}
    for u in users:
        users_by_org.setdefault(u.organization_id, []).append(u)

    #Create kudos in bulk
    kudos_list = []
    for org_id, org_users in users_by_org.items():
        for giver in org_users:
            receivers = [u for u in org_users if u.id != giver.id]
            for _ in range(random.randint(1, 3)):
                if giver.kudos_remaining > 0 and receivers:
                    receiver = random.choice(receivers)
                    kudos_list.append(Kudos(
                        giver_id=giver.id,
                        receiver_id=receiver.id,
                        message=random.choice(messages),
                        created_at=get_random_past_datetime(weeks_back=8)
                    ))
                    giver.kudos_remaining -= 1

    session.add_all(kudos_list)

    #Commit once at the end
    session.commit()
