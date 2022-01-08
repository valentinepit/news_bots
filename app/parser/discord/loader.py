import discord
import asyncio
import os
from datetime import datetime, timedelta

TOKEN_AUTH = os.environ['DISCORD_TOKEN']

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
    now = datetime.now()
    for channel_name, channel_id in channels.items():
        channel = client.get_channel(channel_id)
        messages = await channel.history(limit=2).flatten()
        for msg in messages:
            if now < msg.created_at + timedelta(minutes=10):
                print(f'{channel_name}\n{msg.created_at}')
                print('-' * 50)
    await client.close()

client.run(TOKEN_AUTH, bot=False)
