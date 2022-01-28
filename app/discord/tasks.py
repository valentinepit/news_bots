import asyncio

from app.celery import app
from app.discord.loader import update_news


@app.task(ignore_result=True)
def get_news():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_news())
