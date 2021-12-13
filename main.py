import logging

from tasks import update_news, test

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    update_news()
    test()
