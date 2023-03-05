import os

from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy import create_engine

from models import Base
from .admin import CurrencyAdmin, OrderAdmin
from .auth_backend import AuthenticationBackend
from .service import create_user

app = FastAPI()
engine = create_engine(
    "sqlite:////db/example.db",
    connect_args={"check_same_thread": False},
)
authentication_backend = AuthenticationBackend(secret_key="gphkfdbptvfswcr", engine=engine)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(CurrencyAdmin)
admin.add_view(OrderAdmin)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(engine)
    create_user(engine, os.environ["USER"], os.environ["PASSWORD"])
