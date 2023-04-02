from models import Currency, Order


class BaseExchange:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def place_order(self, currency: Currency) -> Order:
        order = self.place_order(currency)
        order.save()
        return order

    def _place_order(self, currency: Currency) -> Order:
        raise NotImplemented
