from logging import getLogger

from binance.error import ClientError
from binance.spot import Spot
from models import Currency, Order, Side

from .base import BaseExchange


class Exchange(BaseExchange):
    @property
    def account(self) -> Spot:
        return Spot(api_key=self.api_key, api_secret=self.api_secret)

    def _place_order(self, currency: Currency) -> Order:
        price = float(self.account.avg_price(currency.symbol)["price"])
        try:
            self.account.new_order(
                symbol=f"{currency.symbol}",
                side="BUY",
                type="MARKET",
                quoteOrderQty=currency.amount_in_base,
            )
        except ClientError as error:
            logger.warning("Failed to place order: %s", error)

        return Order(
            currency=currency,
            amount=1/price*currency.amount_in_base,
            price=price,
            side=Side.buy,
        )
