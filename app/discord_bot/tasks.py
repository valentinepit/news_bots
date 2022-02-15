import asyncio

from app.celery import app
from app.discord_bot.loader import update_news


@app.task()
async def get_news():
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(update_news())
    await update_news()