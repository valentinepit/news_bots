import logging
import os

from celery import Celery
from celery.schedules import crontab

app = Celery(
    "app",
    broker=os.environ["CELERY_BROKER_URL"],
    include=["app.notion.tasks", "app.discord.tasks"],
)

app.conf.beat_schedule = {
    "notion-update_news-every-5-minutes": {
        "task": "app.notion.tasks.update_news",
        "schedule": crontab(minute="*/5"),
        "options": {"expires": 60 * 5},
    },
    "discord-update_news-every-5-minutes": {
        "task": "app.discord.tasks.update",
        "schedule": crontab(minute="*/5"),
        "options": {"expires": 60 * 5},
    },
}

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    app.start()
