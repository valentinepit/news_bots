import asyncio
import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import aioschedule
from discord_bot import update_news

TG_TOKEN = os.environ["TG_ANALYTICS_TOKEN"]
CHANNEL_ID = os.environ["ANALYTICS_CHANNEL_ID"]

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

logger = logging.getLogger(__name__)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


async def send_message(msg, ch_id):
    await bot.send_message(ch_id, msg)


async def scheduler():
    aioschedule.every(1).minutes.do(get_discord_news)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())


async def get_discord_news():
    _news = await update_news()



def start_bot():
    executor.start_polling(dp, on_startup=on_startup)


if __name__ == "__main__":
    start_bot()
