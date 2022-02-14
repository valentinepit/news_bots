import logging

from app.discord.tasks import get_news as discord
from app.notion.tasks import get_news as notion
from app.tg_bot.discord_handler import start_bot

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # discord()
    # notion()
    start_bot()

