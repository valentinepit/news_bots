from app.celery import app
from app.parser.notion import News


@app.task
def update_news():
    News().update_news()


