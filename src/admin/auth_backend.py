import hashlib

from sqladmin.authentication import AuthenticationBackend as BaseBackend
from sqlalchemy import select

from starlette.requests import Request
from models import User, engine
from sqlalchemy.orm import Session


class AuthenticationBackend(BaseBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if not username or not password:
            return False

        hash_password = hashlib.sha256(password.encode()).hexdigest()

        with Session(engine) as session:
            user = session.scalars(select(User).where(User.username == username).where(User.password == hash_password)).all()
            if not user:
                return False

        request.session.update({"user": username})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user = request.session.get("user")

        if not user:
            return False

        return True

