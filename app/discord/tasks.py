from app.celery import app
from app.discord.loader import update_news


@app.task(ignore_result=True)
def get_news():
    update_news()
