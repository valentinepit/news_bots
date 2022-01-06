import logging
import os

import discord

from app.tg_bot.aio_bot import NewsBot

logging.basicConfig(level=logging.INFO)

discord_id = {
    'bent': 913416871380938814
}

TOKEN = os.environ['DISCORD_TOKEN']
channel_id = os.environ["ANALYTICS_CHANNEL_ID"]

client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client}')


@client.event
async def on_message(message):
    tg_msg = f"From {message.author}\n{message.content.lstrip('@everyone ')}"
    bot = NewsBot()
    await bot.send_message(tg_msg)


client.run(TOKEN)
