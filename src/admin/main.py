import os

from fastapi import FastAPI
from sqladmin import Admin

from models import Base, engine
from .admin import CurrencyAdmin, OrderAdmin
from .auth_backend import AuthenticationBackend
from .service import create_user

app = FastAPI()
authentication_backend = AuthenticationBackend(secret_key="gphkfdbptvfswcr")

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(CurrencyAdmin)
admin.add_view(OrderAdmin)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(engine)
    create_user(os.environ["USER"], os.environ["PASSWORD"])
