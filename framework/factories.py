from uuid import uuid4

from faker import Faker

fake = Faker()


def new_user() -> dict:
    """Credentials for a not-yet-existing user. Unique per call, safe for parallel runs."""
    suffix = uuid4().hex[:8]
    return {
        "username": f"{fake.first_name().lower()}_{suffix}",
        "email": f"{suffix}@example.com",
        "password": fake.password(length=12),
    }
