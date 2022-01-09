from app.celery import app
from app.discord.loader import update_news


@app.task
def get_news():
    update_news()
