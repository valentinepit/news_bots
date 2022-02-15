import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict

from discord.errors import Forbidden
from discord.ext import commands
from discord_bot import message_editor

TOKEN_AUTH = os.environ["DISCORD_TOKEN"]
TG_TOKEN = os.environ["TG_ANALYTICS_TOKEN"]
CHANNEL_ID = os.environ["ANALYTICS_CHANNEL_ID"]

logger = logging.getLogger(__name__)

last_check = None

channels_list_path = "discord_bot/discord_channels.json"
channels = {}


async def update_news():
    client = commands.Bot(command_prefix="!", reconnect=True)
    try:
        await client.login(TOKEN_AUTH, bot=False)
        _news = await collect_messages_from_channels(client)
    finally:
        await client.close()
    logger.info(f"{len(_news)} news loaded from Discord")
    return _news


async def collect_messages_from_channels(client):
    now = datetime.now()
    messages = []
    global last_check, channels
    channels = json.loads(open(channels_list_path, "r").read())
    last_check = last_check or now - timedelta(minutes=10)
    logger.info(f"last_chek = {last_check}")
    for channel_name, channel_id in channels.items():
        try:
            channel = await client.fetch_channel(channel_id)
        except Forbidden:
            logger.info(f"Can't connect to {channel_name}")
            continue

        logger.info(f"connected to {channel_name}")
        msgs = await channel.history(after=last_check).flatten()
        for msg in msgs:
            message = message_editor.convert_row_news(msg.content, channel.guild)
            created_at = msg.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            messages.append(f"{channel_name}\n{created_at}\n{message}")
    last_check = now
    return messages


async def update_channels(add_ch: Dict, del_ch: str):
    if not add_ch and not del_ch:
        return None
    for ch in add_ch:
        channels[ch["name"]] = int(ch["id"])
        logger.info(f"Added channel {ch['name']} with id {ch['id']}")
    for ch in del_ch:
        if ch in channels:
            try:
                deleted_channel = channels.pop(ch)
                logger.info(f"Deleted channel {ch} with id {deleted_channel}")
            except KeyError:
                logger.info(f"Can't delete channel {ch}")
    with open(channels_list_path, "w", encoding="utf-8") as ch_file:
        json.dump(channels, ch_file, ensure_ascii=False)
    return True
