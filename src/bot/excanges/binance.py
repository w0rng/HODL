from typing import Type

from binance.spot import Spot
from models import Currency, Order, engine, Side
from sqlalchemy.orm import Session


class Exchange:
    def __init__(self, api_key: str, api_secret: str):
        self.client = Spot(api_key=api_key, api_secret=api_secret)

    def place_order(self, currency: Type[Currency]):
        self.client.new_order(
            symbol=f"{currency.symbol}",
            side="BUY",
            type="MARKET",
            quoteOrderQty=currency.amount_in_base,
        )
        with Session(engine) as session:
            price = float(self.client.avg_price(currency.symbol)["price"])
            session.add(
                Order(
                    currency=currency,
                    amount=1/price*currency.amount_in_base,
                    price=price,
                    side=Side.buy,
                )
            )
            session.commit()
