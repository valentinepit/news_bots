import logging
import os

from celery import Celery
from celery.schedules import crontab

app = Celery(
    "app",
    broker=os.environ["CELERY_BROKER_URL"],
    include=["app.tg_bot.tasks", "app.discord_bot.tasks", "app.notion.tasks"],
)

app.conf.worker_prefetch_multiplier = 1

app.conf.beat_schedule = {
    "notion-update_news-every-5-minutes": {
        "task": "app.notion.tasks.get_news",
        "schedule": crontab(minute="*/5"),
        "options": {"expires": 60 * 5},
    },
    # "start_discord_bot_once_a day": {
    #     "task": "app.tg_bot.tasks.start",
    #     "schedule": crontab(),
    #     "options": {"expires": 60 * 5},
    # },
    "discord_bot-update_news-every-10-minutes": {
        "task": "app.discord_bot.tasks.get_news",
        "schedule": crontab(minute="*/1"),
        "options": {"expires": 60 * 5},
    },
}

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    app.start()
