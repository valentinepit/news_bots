import json
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import BadRequest

from notion.message_editor import message_cutter

logger = logging.getLogger(__name__)

discord_bot_update_num = None


class NewsBot:
    token: str
    channel_id: str

    def __init__(self):
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)

    async def send_photo(self, message, photo):
        messages = [message]
        if len(message) > 1024:
            messages = message_cutter(1024, message)
        await self.bot.send_photo(self.channel_id, photo=photo, caption=messages[0], parse_mode="HTML")
        await self.send_multipart_message(messages[1:], disable_web_page_preview=True)

    async def send_message(self, message, parse_mode="HTML"):
        messages = [message]
        if len(message) > 4096:
            messages = message_cutter(4096, message)
        try:
            await self.bot.send_message(self.channel_id, messages[0], parse_mode=parse_mode)
            await self.send_multipart_message(messages[1:], parse_mode=parse_mode)
        except BadRequest:
            await self.bot.send_message(self.channel_id, messages[0], parse_mode="Markdown")
            await self.send_multipart_message(messages[1:], parse_mode="Markdown")

    async def send_multipart_message(self, messages, parse_mode="HTML", disable_web_page_preview=False):
        for _message in messages:
            await self.bot.send_message(
                self.channel_id, _message, disable_web_page_preview=disable_web_page_preview, parse_mode=parse_mode
            )

    async def disconnect(self):
        await self.bot.session.close()


class NotionBot(NewsBot):
    token = os.environ["TG_TOKEN"]
    channel_id = os.environ["CHANNEL_ID"]


class DiscordBot(NewsBot):
    token = os.environ["TG_ANALYTICS_TOKEN"]
    channel_id = os.environ["ANALYTICS_CHANNEL_ID"]

    async def get_updates(self):
        global discord_bot_update_num
        new_channels = []
        channels_for_delete = []
        discord_bot_update_num = discord_bot_update_num or -1
        updates = await self.bot.get_updates(offset=discord_bot_update_num)
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

    async def send_channels_list(self):
        channels_list_path = "app/discord_bot/discord_channels.json"
        channels = json.loads(open(channels_list_path, "r").read())
        msg = "Список активных каналов: \n"
        for _name, _id in channels.items():
            msg += f"{_name} : {_id}\n"
        _updates = await self.bot.get_updates(limit=1)
        await _updates[0].message.answer(msg, Bot.set_current(self.bot))
