import logging
import os
from decimal import getcontext

from celery import Celery
from celery.schedules import crontab

app = Celery(
    "app",
    # broker=os.environ["CELERY_BROKER_URL"],
    broker='amqp://',
    include=[
        "tasks"
    ],
)
app.conf.worker_prefetch_multiplier = 1

# Optional configuration, see the application user guide.
app.conf.beat_schedule = {
    "parse-update_news-every-5-minutes": {
        "task": "tasks.update_news",
        "schedule": crontab(minute="*/1"),
        "options": {"expires": 60 * 5},
    },
    "test-every-1-minutes": {
        "task": "tasks.test",
        "schedule": crontab(minute="*/1"),
        "options": {"expires": 60 * 5},
    },
}

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    getcontext().prec = 200
    app.start()
