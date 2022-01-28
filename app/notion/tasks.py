from app.celery import app
from app.notion.loader import News


@app.task
def get_news():
    News().update_news()
