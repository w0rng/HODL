import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User, engine


def create_user(username: str, password: str):
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    with Session(engine) as session:
        all_users = session.scalars(select(User).where(User.username == username)).all()
        if all_users:
            return
        user = User(username=username, password=hash_password)
        session.add(user)
        session.commit()
