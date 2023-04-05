import logging
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

logger = logging.getLogger(__name__)


class Bot:
    exchange = Exchange(os.environ["API_KEY"], os.environ["SECRET_KEY"])

    @classmethod
    def run(cls):
        logger.info("Running bot")
        requests.post(os.getenv("HEALTH_CHECK"))
        with Session(engine) as session:
            for currency in cls._get_currencies():
                logger.info("Placing order for %s", currency.symbol)
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
                logger.info("Currency %s is not started yet", currency.symbol)
                continue
            if currency.last_update is None:
                logger.info("Currency %s is new", currency.symbol)
                result.append(currency)
                continue
            if currency.last_update + timedelta(seconds=currency.interval) <= datetime.utcnow():
                logger.info("Currency %s is ready to update", currency.symbol)
                result.append(currency)
        return result

    @staticmethod
    def _load_all_currencies() -> list[Currency]:
        with Session(engine) as session:
            return session.query(Currency).all()


def start():
    logger.info("Starting bot")
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
    sentry_logging = sentry_sdk.integrations.logging.LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR,
    )
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DNS"),
        integrations=[
            sentry_logging,
        ],
    )
    start()
