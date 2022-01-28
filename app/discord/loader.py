import logging
import os
from datetime import datetime, timedelta

from app.discord import message_editor
from app.tg_bot.aio_bot import NewsBot
from discord.errors import Forbidden
from discord.ext import commands

TOKEN_AUTH = os.environ["DISCORD_TOKEN"]
TG_TOKEN = os.environ["TG_ANALYTICS_TOKEN"]
CHANNEL_ID = os.environ["ANALYTICS_CHANNEL_ID"]

logger = logging.getLogger(__name__)

channels = {
    "Yarn Talk": 735617936206594249,
    "BENT Finance": 913455858699079740,
    "Angle Protocol": 835068536270487553,
    "Stake DAO": 803667081978708057,
    "Curve Finance": 729810461888872509,
    "Frax Finance": 789823672717541376,
}

last_check = None


async def update_news():
    client = commands.Bot(command_prefix="!", reconnect=True)
    try:
        await client.login(TOKEN_AUTH, bot=False)
        cnt = await collect_messages_from_channels(client)
    finally:
        await client.close()
    logger.info(f"{cnt} news loaded to tg from Discord")


async def collect_messages_from_channels(client):
    now = datetime.now()
    global last_check
    last_check = last_check or now - timedelta(minutes=10)
    bot = NewsBot(TG_TOKEN, CHANNEL_ID)
    channel_for_add, channels_for_delete = await bot.get_updates()
    update_channels(channel_for_add, channels_for_delete)

    cnt = 0
    for channel_name, channel_id in channels.items():
        try:
            channel = await client.fetch_channel(channel_id)
        except Forbidden:
            logger.info(f"Can't connect to {channel_name}")
            continue

        logger.info(f"connected to {channel_name}")
        messages = await channel.history(after=last_check).flatten()
        for msg in messages:
            message = message_editor.convert_row_news(msg.content, channel.guild)
            created_at = msg.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            await bot.send_message(f"{channel_name}\n{created_at}\n{message}")
            cnt += 1
    last_check = now
    await bot.disconnect()
    return cnt


def update_channels(add_ch, del_ch):
    for ch in add_ch:
        channels[ch["name"]] = ch["id"]
        logger.info(f"Added channel {ch['name']} with id {ch['id']}")
    for ch in del_ch:
        if ch in channels:
            deleted_channel = channels.pop(ch)
            logger.info(f"Deleted channel {ch} with id {deleted_channel}")