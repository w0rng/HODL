from binance.spot import Spot
from configs import Settings, Currency


class Exchange:
    def __init__(self, api_key: str, api_secret: str, setting: Settings):
        self.client = Spot(api_key=api_key, api_secret=api_secret)
        self.setting = setting

    def place_order(self, currency: Currency):
        self.client.new_order(
            symbol=f"{currency.name}{self.setting.base_currency}",
            side="BUY",
            type="MARKET",
            quoteOrderQty=currency.count_in_base,
        )