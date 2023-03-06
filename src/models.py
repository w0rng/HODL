import os

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum


Base = declarative_base()
engine = create_engine(
    os.environ["DB_URL"],
    connect_args={"check_same_thread": False},
)

class Side(enum.Enum):
    buy = "BUY"
    sell = "SELL"


class User(Base):
    __tablename__ = "user"

    username = Column(String, primary_key=True, unique=True)
    password = Column(String)


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    amount_in_base = Column(Float)
    start = Column(DateTime, nullable=True, default=datetime.utcnow)
    interval = Column(Integer)
    last_update = Column(DateTime, nullable=True, default=None)

    def __str__(self):
        return self.symbol


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    side = Column(Enum(Side))
    price = Column(Float)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    currency_id = Column(Integer, ForeignKey('currency.id'))
    currency = relationship("Currency", foreign_keys=[currency_id])
