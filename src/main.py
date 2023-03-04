from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from logging import getLogger, DEBUG

from sqlalchemy.exc import OperationalError

from configs import my_settings, Currency
from excanges.binance import Exchange
from os import getenv

logger = getLogger(__name__)
logger.setLevel(DEBUG)

store = SQLAlchemyJobStore(url='sqlite:////db/jobs.sqlite')
scheduler = BlockingScheduler(
    jobstores={
        'default': store
    }
)


def buy_crypto(currency: Currency):
    Exchange(getenv("API_KEY"), getenv("SECRET_KEY"), my_settings).\
        place_order(currency)


def load_new_jobs():
    all_jobs = [job.id for job in store.get_all_jobs()]
    for currency in my_settings.currencies:
        if currency.name in all_jobs:
            logger.info("job for %s already exists", currency.name)
            continue
        logger.info("start job for %s", currency.name)
        scheduler.add_job(
            buy_crypto,
            CronTrigger.from_crontab(currency.cron),
            args=(currency,),
            id=currency.name,
        )


def remove_old_jobs():
    all_currencies = [currency.name for currency in my_settings.currencies]
    for job in store.get_all_jobs():
        if job.id not in all_currencies:
            logger.info("remove job for %s", job.id)
            scheduler.remove_job(job.id)


def main():
    try:
        load_new_jobs()
        remove_old_jobs()
    except OperationalError:
        logger.warning("database is not ready yet")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    main()
