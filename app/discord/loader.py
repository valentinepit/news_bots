import logging
import os
from datetime import datetime, timedelta

import discord
from aiogram.exceptions import TelegramBadRequest

from app.discord import message_editor
from app.tg_bot.aio_bot import NewsBot

TOKEN_AUTH = os.environ["DISCORD_TOKEN"]
TG_TOKEN = os.environ["TG_ANALYTICS_TOKEN"]
CHANNEL_ID = os.environ["ANALYTICS_CHANNEL_ID"]

logger = logging.getLogger(__name__)

client = discord.Client()

channels = {
    "Yarn Talk": [735617936206594249, "734804446353031319"],
    "BENT Finance": [913455858699079740, "913416871380938814"],
    "Angle Protocol": [835068536270487553, "835066439891157012"],
    "Stake DAO": [803667081978708057, "802495248563044372"],
    "Curve Finance": [729810461888872509, "729808684359876718"],
    "Frax Finance": [789823672717541376, "789823126966894612"],
}


@client.event
async def on_ready():
    logger.info(f"We have logged in as {client}")
    cnt = await collect_messages_from_channels()
    logger.info(f"{cnt} news loaded to tg")
    await client.close()


@client.event
async def collect_messages_from_channels():
    now = datetime.now()
    bot = NewsBot(TG_TOKEN, CHANNEL_ID)
    cnt = 0
    for channel_name, channel_id in channels.items():
        channel = client.get_channel(channel_id[0])
        logger.info(f"connected to {channel_name}")
        messages = await channel.history(limit=3).flatten()
        for msg in messages:
            if now > msg.created_at + timedelta(minutes=10):
                message = message_editor.convert_row_news(msg.content, channel_id[1])
                try:
                    await bot.send_message(f"{channel.guild}\n{message}")
                # TODO: find exception
                except TelegramBadRequest:
                    await bot.send_message(f"{channel_name}\n{message}", parse_mode="Markdown")
                cnt += 1
    await bot.close_connection()
    return cnt


def update_news():
    client.run(TOKEN_AUTH, bot=False)
