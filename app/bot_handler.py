import asyncio
import json
import os

import aioschedule
import sentry_sdk
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import BadRequest

from config import logger
from discord_bot import update_news as discord
from gov_prop.loader import get_news as gov_prop
from gov_prop.loader import source_list_path
from notion.expl.loader import update_exploits as exploits
from notion.loader import News
from notion.message_editor import message_cutter
from twitter.loader import TwitterNews

TG_TOKEN = os.environ["TG_ANALYTICS_TOKEN"]
ANALYTICS_ID = os.environ["ANALYTICS_CHANNEL_ID"]
NEWS_ID = os.environ["CHANNEL_ID"]
TWITTER_ID = os.environ["TWITTER_CHANNEL_ID"]

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

discord_channels_path = "discord_bot/discord_channels.json"


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply("Введите /help для получения списка команд")


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply(
        "/discord - Список текущих каналов \n"
        "/add_discord - Добавить канал (Name:id) \n"
        "/delete_discord - Убрать канал (Name) \n"
        "/governance - Список governance сайтов \n"
        "/add_governance - Добавить сайт (Name:url) \n"
        "/delete_governance - Убрать сайт (Name) \n"
        "/proposal - Список proposal сайтов \n"
        "/add_proposal - Добавить сайт (Name:url)\n"
        "/delete_proposal - Убрать сайт (Name) \n"
        "/twitter - Список twitter аккаунтов \n"
        "/add_twitter - Добавить аккаунт (Name)\n"
        "/delete_twitter - Убрать аккаунт (Name) \n"
    )


@dp.message_handler(commands=["discord"])
async def process_channels_command(message: types.Message):
    channels = json.loads(open(discord_channels_path, "r").read())
    msg = "Список активных каналов: \n"
    for _name, _id in channels.items():
        msg += f"{_name} : {_id}\n"
    await message.reply(msg)


@dp.message_handler(commands=["add_discord"])
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


@dp.message_handler(commands=["delete_discord", "delete_governance", "delete_proposal"])
async def process_delete_source_command(message: types.Message):
    if message.get_command() == "/delete_discord":
        path = discord_channels_path
    else:
        path = source_list_path
    with open(path, "r") as f:
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


@dp.message_handler(commands=["governance", "proposal", "twitter"])
async def process_gov_prop_command(message: types.Message):
    channels = json.loads(open(source_list_path, "r").read())
    msg = "Список активных каналов: \n"
    if message.get_command() == "/twitter":
        tw = TwitterNews()
        for source in tw.sources:
            msg += f"{source}\n"
    for _name, description in channels.items():
        if message.get_command() == "/governance" and description[1] == "gov":
            msg += f"{_name} : {description[0]}\n"
        elif message.get_command() == "/proposal" and description[1] == "prop":
            msg += f"{_name} : {description[0]}\n"
            pass
    await message.reply(msg)


@dp.message_handler(commands=["add_governance", "add_proposal"])
async def process_add_site_command(message: types.Message):
    with open(source_list_path, "r") as f:
        data = json.load(f)
    if message.get_command() == "/add_governance":
        site_type = "gov"
    else:
        site_type = "prop"
    try:
        channel_ids = message.get_args().split(":")
        data[channel_ids[0]] = [channel_ids[1].strip(), site_type]
        with open(source_list_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        msg = f"Добавлен новый канал {channel_ids[0]}"
    except (IndexError, ValueError):
        msg = "Параметры должны быть в виде Channel name: Channel url"
    await message.reply(msg)


@dp.message_handler(commands=["delete_twitter"])
async def process_add_twitter_command(message: types.Message):
    tw = TwitterNews()
    try:
        channel_id = message.get_args()
        _name = tw.sources.pop(channel_id)
        msg = f"Удален канал {_name}"
    except (IndexError, ValueError):
        msg = "Параметры должны быть в виде Channel name"
    await message.reply(msg)


@dp.message_handler(commands=["add_twitter"])
async def process_delete_twitter_command(message: types.Message):
    tw = TwitterNews()
    try:
        channel_id = message.get_args()
        tw.sources[channel_id] = None
        msg = f"Добавлен новый канал {channel_id}"
    except (IndexError, ValueError):
        msg = "Параметры должны быть в виде Channel name"
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
    aioschedule.every(10).minutes.do(update_twitter_news)
    aioschedule.every(10).minutes.do(update_notion_news)
    aioschedule.every().day.at("10:10").do(update_exploits)
    aioschedule.every().day.at("10:20").do(update_gov_prop_news)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())


async def update_exploits():
    cnt = exploits()
    logger.info(f"uploaded {cnt} items to Notion")


async def update_notion_news():
    notion_news = News()
    msgs = notion_news.update_news()
    for msg in msgs:
        if msg["photo"]:
            await send_photo(msg["text"], msg["photo"], NEWS_ID)
        else:
            await send_message(msg["text"], NEWS_ID)


async def update_discord_news():
    msgs = await discord()
    for msg in msgs:
        await send_message(msg, ANALYTICS_ID)


async def update_gov_prop_news():
    _news = gov_prop()
    for name, msgs in _news.items():
        for msg in msgs:
            await send_message(f"<b>{name}</b>\n{msg}", ANALYTICS_ID)


async def update_twitter_news():
    twitter_news = TwitterNews()
    msgs = []
    try:
        msgs = twitter_news.update_news()
    except Exception as e:
        sentry_sdk.capture_exception(e)
    for msg in msgs:
        await send_message(msg, TWITTER_ID)


def start_bot():
    executor.start_polling(dp, on_startup=on_startup)


if __name__ == "__main__":
    start_bot()
