import os

from aiogram import Bot, Dispatcher

bot_token = os.environ["TG_TOKEN"]
channel_id = os.environ["CHANNEL_ID"]

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


class NewsBot:

    @dp.message_handler()
    async def send_photo(self, message, photo):
        await bot.send_photo(channel_id, photo=photo, caption=message, parse_mode='HTML')

    @dp.message_handler()
    async def send_message(self, message):
        await bot.send_message(channel_id, message, parse_mode='HTML')
