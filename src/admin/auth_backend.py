import hashlib

from sqladmin.authentication import AuthenticationBackend as BaseBackend
from sqlalchemy import Engine, select

from starlette.requests import Request
from models import User
from sqlalchemy.orm import Session


class AuthenticationBackend(BaseBackend):
    def __init__(self, secret_key: str, engine: Engine) -> None:
        super().__init__(secret_key=secret_key)
        self.engine = engine

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if not username or not password:
            return False

        hash_password = hashlib.sha256(password.encode()).hexdigest()

        with Session(self.engine) as session:
            user = session.scalars(select(User).where(User.username == username).where(User.password == hash_password)).all()
            if not user:
                return False

        request.session.update({"user": username})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user = request.session.get("user")

        if not user:
            return False

        # Check the token
        return True

