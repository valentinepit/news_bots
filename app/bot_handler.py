import asyncio
import json
import logging
import os

import aioschedule
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import BadRequest
from discord_bot import update_news as discord
from notion import News
from notion.message_editor import message_cutter

TG_TOKEN = os.environ["TG_ANALYTICS_TOKEN"]
CHANNEL_ID = os.environ["ANALYTICS_CHANNEL_ID"]

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

logger = logging.getLogger(__name__)
discord_channels_path = "app/discord_bot/discord_channels.json"


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply("Введите /help для получения списка команд")


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply(
        "/channels - Вывдодит список текущих каналов \n"
        "/add_channel - Добавить канал (Name:id) \n"
        "/delete_channel - Убрать канал (Name)"
    )


@dp.message_handler(commands=["channels"])
async def process_channels_command(message: types.Message):
    channels = json.loads(open(discord_channels_path, "r").read())
    msg = "Список активных каналов: \n"
    for _name, _id in channels.items():
        msg += f"{_name} : {_id}\n"
    await message.reply(msg)


@dp.message_handler(commands=["add_channel"])
async def process_add_channel_command(message: types.Message):
    with open(discord_channels_path, "r") as f:
        data = json.load(f)
    try:
        channel_ids = message.get_args().split(":")
        data[channel_ids[0]] = int(channel_ids[1].strip())
        with open(discord_channels_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        msg = f"Добавлен новый канал {channel_ids[0]}"
    except (IndexError, ValueError):
        msg = "Параметры должны быть в виде Channel name: Channel id"
    await message.reply(msg)


@dp.message_handler(commands=["delete_channel"])
async def process_delete_channel_command(message: types.Message):
    with open(discord_channels_path, "r") as f:
        data = json.load(f)
        channel_name = message.get_args()
    try:
        name = data.pop(channel_name)
        with open(discord_channels_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        msg = f"Удален канал id - {name}"
    except KeyError:
        msg = "Не удается найти канал с таким названием"
    await message.reply(msg)


async def send_photo(message, photo, channel_id):
    messages = [message]
    if len(message) > 1024:
        messages = message_cutter(1024, message)
    await bot.send_photo(channel_id, photo=photo, caption=messages[0], parse_mode="HTML")
    await send_multipart_message(messages[1:], channel_id, disable_web_page_preview=True)


async def send_message(message, channel_id, parse_mode="HTML"):
    messages = [message]
    if len(message) > 4096:
        messages = message_cutter(4096, message)
    try:
        await bot.send_message(channel_id, messages[0], parse_mode=parse_mode)
        await send_multipart_message(messages[1:], channel_id, parse_mode=parse_mode)
    except BadRequest:
        await bot.send_message(channel_id, messages[0], parse_mode="Markdown")
        await send_multipart_message(messages[1:], channel_id, parse_mode="Markdown")


async def send_multipart_message(messages, channel_id, parse_mode="HTML", disable_web_page_preview=False):
    for _message in messages:
        await bot.send_message(
            channel_id, _message, disable_web_page_preview=disable_web_page_preview, parse_mode=parse_mode
        )


async def scheduler():
    aioschedule.every(5).minutes.do(update_discord_news)
    aioschedule.every(60).seconds.do(update_notion_news)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())


async def update_notion_news():
    notion_news = News()
    msgs = notion_news.update_news()
    for msg in msgs:
        if msg["photo"]:
            await send_photo(msg["text"], msg["photo"], CHANNEL_ID)
        else:
            await send_message(msg["text"], CHANNEL_ID)


async def update_discord_news():
    msgs = await discord()
    for msg in msgs:
        await send_message(msg, CHANNEL_ID)


def start_bot():
    executor.start_polling(dp, on_startup=on_startup)


if __name__ == "__main__":
    start_bot()
