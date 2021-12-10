from pprint import pprint

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot_token = '5034223897:AAGj1NPq3LrSrng4kyUIuC1gQk_0OWDu1S4'
channel_id = '@warp_news'

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


class NewsBot:

    @dp.message_handler()
    async def send_message(self, message):
        await bot.send_message(channel_id, message, parse_mode=types.ParseMode.HTML)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
