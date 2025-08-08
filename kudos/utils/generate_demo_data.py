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

    # 1️⃣ Create organizations (bulk)
    orgs = [Organization(name=name) for name in org_names]
    session.add_all(orgs)
    session.flush()  # Get IDs without committing yet

    # 2️⃣ Create users for all orgs (bulk)
    users = []
    for org in orgs:
        for _ in range(random.randint(3, 5)):
            users.append(User(
                username=faker.user_name(),
                email=faker.email(),
                password=bcrypt.hash(faker.password()),  # hash here if needed
                organization_id=org.id,
                kudos_remaining=3
            ))
    session.add_all(users)
    session.flush()  # Assign IDs without committing

    # 3️⃣ Map users by org for kudos generation
    users_by_org = {}
    for u in users:
        users_by_org.setdefault(u.organization_id, []).append(u)

    # 4️⃣ Create kudos in bulk
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

# faker = Faker()

# def get_random_past_datetime(weeks_back=8):
#     """Return a random datetime in the past `weeks_back` weeks."""
#     now = datetime.utcnow()
#     start_date = now - timedelta(weeks=weeks_back)
#     # Random time between start_date and now
#     random_seconds = random.randint(0, int((now - start_date).total_seconds()))
#     return start_date + timedelta(seconds=random_seconds)

# def generate_demo_data(session: Session):
#     org_names = ["Alpha Org", "Beta Org", "Gamma Org"]
#     messages = [
#         "Great job!",
#         "Amazing work!",
#         "Thanks for helping!",
#         "Well done!",
#         "Incredible effort!",
#     ]

#     # Create organizations
#     orgs = []
#     for name in org_names:
#         org = Organization(name=name)
#         session.add(org)
#         orgs.append(org)
#     session.commit()

#     # Create users in each organization
#     users_by_org = {}
#     for org in orgs:
#         users = []
#         for _ in range(random.randint(3, 5)):
#             user = User(
#                 username=faker.user_name(),
#                 email=faker.email(),
#                 password=faker.password(),
#                 organization_id=org.id,
#                 kudos_remaining=3
#             )
#             session.add(user)
#             users.append(user)
#         users_by_org[org.id] = users
#     session.commit()

#     # Give kudos randomly across past N weeks and times
#     for org_id, users in users_by_org.items():
#         for giver in users:
#             receivers = [u for u in users if u.id != giver.id]
#             for _ in range(random.randint(1, 3)):
#                 if giver.kudos_remaining > 0 and receivers:
#                     receiver = random.choice(receivers)
#                     created_at = get_random_past_datetime(weeks_back=8)

#                     kudos = Kudos(
#                         giver_id=giver.id,
#                         receiver_id=receiver.id,
#                         message=random.choice(messages),
#                         created_at=created_at
#                     )
#                     session.add(kudos)
#                     giver.kudos_remaining -= 1
#     session.commit()
