import enum
import os
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, relationship

Base = declarative_base()
engine = create_engine(
    os.environ["DB_URL"],
    connect_args={"check_same_thread": False},
)


class Side(enum.Enum):
    buy = "BUY"
    sell = "SELL"


class Savable(Base):
    __abstract__ = True

    def save(self):
        with Session(engine) as session:
            session.add(self)
            session.commit()


class User(Savable):
    __tablename__ = "user"

    username = Column(String, primary_key=True, unique=True)
    password = Column(String)


class Currency(Savable):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    amount_in_base = Column(Float)
    start = Column(DateTime, nullable=True, default=datetime.utcnow)
    interval = Column(Integer)
    last_update = Column(DateTime, nullable=True, default=None)

    def __str__(self):
        return self.symbol


class Order(Savable):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    side = Column(Enum(Side))
    price = Column(Float)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    currency_id = Column(Integer, ForeignKey("currency.id"))
    currency = relationship("Currency", foreign_keys=[currency_id])
