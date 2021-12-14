import logging

from app.parser.tasks import update_news

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    update_news()
