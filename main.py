import logging

from app.parser.tasks import update_news

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    update_news()