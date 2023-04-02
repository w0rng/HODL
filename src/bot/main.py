import os
from datetime import datetime, timedelta
from typing import Type

import requests
import sentry_sdk
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.excanges.binance import Exchange
from models import Currency, engine
from sqlalchemy.orm import Session


class Bot:
    exchange = Exchange(os.environ["API_KEY"], os.environ["SECRET_KEY"])

    @classmethod
    def run(cls):
        requests.post(os.getenv("HEALTH_CHECK"))
        with Session(engine) as session:
            for currency in cls._get_currencies():
                cls.exchange.place_order(currency)
                currency.last_update = datetime.utcnow()
                session.add(currency)
            session.commit()

    @classmethod
    def _get_currencies(cls) -> list[Type[Currency]]:
        all_currencies = cls._load_all_currencies()
        return cls._filer_currencies(all_currencies)

    @staticmethod
    def _filer_currencies(currencies: list[Type[Currency]]) -> list[Type[Currency]]:
        result = []
        for currency in currencies:
            if datetime.utcnow() < currency.start:
                continue
            if currency.last_update is None:
                result.append(currency)
                continue
            if currency.last_update + timedelta(seconds=currency.interval) <= datetime.utcnow():
                result.append(currency)
        return result

    @staticmethod
    def _load_all_currencies() -> list[Currency]:
        with Session(engine) as session:
            return session.query(Currency).all()


def start():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        Bot.run,
        CronTrigger.from_crontab("* * * * *"),
    )
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    sentry_sdk.init(os.getenv("SENTRY_DNS"))
    start()
