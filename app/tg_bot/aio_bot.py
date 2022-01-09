from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramRetryAfter
from time import sleep


class NewsBot:
    def __init__(self, token, channel_id):
        self.token = token
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(isolate_events=True)
        self.ch_id = channel_id

    async def send_photo(self, message, photo):
        await self.bot.send_photo(self.ch_id, photo=photo, caption=message, parse_mode="HTML")

    async def send_message(self, message, parse_mode="HTML"):
        try:
            await self.bot.send_message(self.ch_id, message, parse_mode=parse_mode)
        except TelegramRetryAfter:
            sleep(50)
            await self.bot.send_message(self.ch_id, message, parse_mode=parse_mode)

    async def close_connection(self):
        await self.bot.session.close()
