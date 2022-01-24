import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import BadRequest

logger = logging.getLogger(__name__)

discord_bot_update_num = 481561451


class NewsBot:
    def __init__(self, token, channel_id):
        self.token = token
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)
        self.ch_id = channel_id

    async def get_updates(self):
        global discord_bot_update_num
        updates = await self.bot.get_updates(offset=discord_bot_update_num)
        new_channels = []
        channels_for_delete = []
        for update in updates:
            logger.info(f"New update available : {update.update_id}")
            try:
                channel_ids = update.message.get_args().split(":")
            except AttributeError:
                channel_ids = update.message.get_args()
            if update.message.get_command() == "/add_channel":
                try:
                    new_channels.append({"name": channel_ids[0], "id": channel_ids[1]})
                except IndexError:
                    continue
            elif update.message.get_command() == "/delete_channel":
                channels_for_delete.append(channel_ids[0])

            discord_bot_update_num = update.update_id + 1

        return new_channels, channels_for_delete

    async def send_photo(self, message, photo):
        await self.bot.send_photo(self.ch_id, photo=photo, caption=message, parse_mode="HTML")

    async def send_message(self, message, parse_mode="HTML", disable_web_page_preview=False):
        try:
            await self.bot.send_message(
                self.ch_id, message, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview
            )
        except BadRequest:
            await self.bot.send_message(
                self.ch_id, message, parse_mode="Markdown", disable_web_page_preview=disable_web_page_preview
            )

    async def disconnect(self):
        await self.bot.session.close()
