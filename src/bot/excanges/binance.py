from typing import Type

from binance.spot import Spot
from models import Currency


class Exchange:
    def __init__(self, api_key: str, api_secret: str):
        self.client = Spot(api_key=api_key, api_secret=api_secret)

    def place_order(self, currency: Type[Currency]):
        response = self.client.new_order(
            symbol=f"{currency.symbol}",
            side="BUY",
            type="MARKET",
            quoteOrderQty=currency.amount_in_base,
        )
        print(response, flush=True)
