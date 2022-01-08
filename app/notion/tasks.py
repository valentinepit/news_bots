from app.celery import app
from app.notion.notion import News


@app.task
def update_news():
    News().update_news()
