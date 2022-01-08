import logging
import os
from datetime import datetime, timedelta

import discord

from app.tg_bot.aio_bot import NewsBot

TOKEN_AUTH = os.environ["DISCORD_TOKEN"]
TG_TOKEN = os.environ["TG_ANALYTICS_TOKEN"]
CHANNEL_ID = os.environ["ANALYTICS_CHANNEL_ID"]

logger = logging.getLogger(__name__)

client = discord.Client()

channels = {
    "Yarn Talk": 735617936206594249,
    "BENT Finance": 913455858699079740,
    "Angle Protocol": 835068536270487553,
    "Stake DAO": 803667081978708057,
    "Curve Finance": 729810461888872509,
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
        channel = client.get_channel(channel_id)
        messages = await channel.history(limit=2).flatten()
        for msg in messages:
            if now < msg.created_at + timedelta(minutes=10):
                try:
                    await bot.send_message(f"{channel_name}\n{msg.content}")
                # TODO: find exception
                except Exception as e:
                    logger.info(f"{e} is an Error in message")
                    await bot.send_message(f"{channel_name}\n{msg.content}", parse_mode="Markdown")
                cnt += 1
    await bot.close_connection()
    return cnt


def update_news():
    client.run(TOKEN_AUTH, bot=False)
