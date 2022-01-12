import logging
import os
from datetime import datetime, timedelta

from aiogram.exceptions import TelegramBadRequest
from discord.ext import commands

from app.discord import message_editor
from app.tg_bot.aio_bot import NewsBot

TOKEN_AUTH = os.environ["DISCORD_TOKEN"]
TG_TOKEN = os.environ["TG_ANALYTICS_TOKEN"]
CHANNEL_ID = os.environ["ANALYTICS_CHANNEL_ID"]

logger = logging.getLogger(__name__)

client = commands.Bot(command_prefix='!', reconnect=True)

channels = {
    "Yarn Talk": 735617936206594249,
    "BENT Finance": 913455858699079740,
    "Angle Protocol": 835068536270487553,
    "Stake DAO": 803667081978708057,
    "Curve Finance": 729810461888872509,
    "Frax Finance": 789823672717541376,
    "Test": 928618938743541823
}


def update_news():
    client.run(TOKEN_AUTH, bot=False)


@client.event
async def on_ready():
    logger.info(f"We have logged in as {client}")
    cnt = await collect_messages_from_channels()
    logger.info(f"{cnt} news loaded to tg")


async def collect_messages_from_channels():
    now = datetime.now()
    time_shift = now - timedelta(minutes=10)
    bot = NewsBot(TG_TOKEN, CHANNEL_ID)
    cnt = 0
    for channel_name, channel_id in channels.items():
        channel = client.get_channel(channel_id)
        logger.info(f"connected to {channel_name}")
        messages = await channel.history(after=time_shift).flatten()
        for msg in messages:
            message = message_editor.convert_row_news(msg.content, channel.guild)
            created_at = msg.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            try:
                await bot.send_message(f"{channel.guild}\n{created_at}\n{message}")
            except TelegramBadRequest:
                await bot.send_message(f"{channel_name}\n{created_at}\n{message}", parse_mode="Markdown")
            cnt += 1

    return cnt

