import asyncio

from app.celery import app
from app.tg_bot.discord_handler import start_bot


@app.task(ignore_result=True)
def start():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_bot()())

