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


def new_article() -> dict:
    """Payload for a new article. The title carries a unique suffix because slugs must be unique."""
    return {
        "title": f"{fake.sentence(nb_words=4).rstrip('.')} {uuid4().hex[:6]}",
        "description": fake.sentence(),
        "body": fake.paragraph(nb_sentences=3),
        "tagList": fake.words(nb=2, unique=True),
    }
