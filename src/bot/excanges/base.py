from typing import Optional

from models import Currency, Order


class BaseExchange:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def place_order(self, currency: Currency) -> Optional[Order]:
        order = self._place_order(currency)
        if not order:
            return None
        order.save()
        return order

    def _place_order(self, currency: Currency) -> Optional[Order]:
        raise NotImplemented
