import logging
import os
from celery import Celery
from celery.schedules import crontab

app = Celery(
    "app",
    broker=os.environ["CELERY_BROKER_URL"],
    include=[
        "app.parser.tasks",
    ],
)

# Optional configuration, see the application user guide.
app.conf.beat_schedule = {
    "parse-update_news-every-5-minutes": {
        "task": "app.parser.tasks.update_news",
        "schedule": crontab(minute="*/5"),
        "options": {"expires": 60 * 5},
    },
}

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app.start()
