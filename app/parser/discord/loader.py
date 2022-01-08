import os
from datetime import datetime, timedelta

import discord

from app.tg_bot.aio_bot import NewsBot

TOKEN_AUTH = os.environ['DISCORD_TOKEN']
TG_TOKEN = os.environ['TG_ANALYTICS_TOKEN']
CHANNEL_ID = os.environ['ANALYTICS_CHANNEL_ID']

client = discord.Client()

channels = {
    'Yarn Talk': 735617936206594249,
    'BENT Finance': 913455858699079740,
    'Angle Protocol': 835068536270487553,
    'Stake DAO': 803667081978708057,
    'Curve Finance': 729810461888872509
}


@client.event
async def on_ready():
    print(f'We have logged in as {client}')
    await collect_messages_from_channels()
    await client.close()


@client.event
async def collect_messages_from_channels():
    now = datetime.now()
    bot = NewsBot(TG_TOKEN, CHANNEL_ID)

    for channel_name, channel_id in channels.items():
        channel = client.get_channel(channel_id)
        messages = await channel.history(limit=2).flatten()
        for msg in messages:
            # INFO: change > to < in prod
            if now > msg.created_at + timedelta(minutes=10):
                try:
                    await bot.send_message(f'{channel_name}\n{msg.content}')
                except Exception as e:
                    print(e)
                    await bot.send_message(f'{channel_name}\n{msg.content}', parse_mode='Markdown')
                    print(f'{channel_name}\n{msg.content}')
                    print('-' * 50)


client.run(TOKEN_AUTH, bot=False)
