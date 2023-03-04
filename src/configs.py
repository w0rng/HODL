from dataclasses import dataclass


@dataclass
class Currency:
    name: str
    cron: str
    count_in_base: int


@dataclass
class Settings:
    currencies: list[Currency]
    base_currency: str


my_settings = Settings(
    base_currency="BUSD",
    currencies=[
        Currency(
            name="ETH",
            cron="0 0 * * 1",
            count_in_base=10,
        ),
        Currency(
            name="DOT",
            cron="0 0 * * 2",
            count_in_base=10,
        ),
        Currency(
            name="BTC",
            cron="0 0 * * 3",
            count_in_base=10,
        ),
        Currency(
            name="BNB",
            cron="0 0 * * 4",
            count_in_base=10,
        ),
    ]
)