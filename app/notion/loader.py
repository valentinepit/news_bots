import asyncio
import json
import logging
import os
from datetime import datetime

import pytz
import requests

import app.notion.message_editor as me
from app.tg_bot.aio_bot import NewsBot

logger = logging.getLogger(__name__)

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DB_ID = os.environ["BASE_ID"]

TG_TOKEN = os.environ["TG_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

BASE_URL = "https://api.notion.com/v1/"

HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json",
}

FILTER = json.dumps({"filter": {"property": "Status", "select": {"equals": "Опубликовать"}}})


class News:
    def read_database(self):
        url = f"{BASE_URL}databases/{DB_ID}/query"
        res = requests.request("POST", url, headers=HEADERS, data=FILTER)
        logger.info(f"We have logged in to Notion")
        data = res.json()
        return data

    def find_news(self, _data):
        public_list = []
        for item in _data["results"]:
            _news = me.convert_row_news(item["properties"])
            _news["id"] = item["id"]
            public_list.append(_news)
        return public_list

    def change_news_status(self, page_id):
        update_url = f"{BASE_URL}pages/{page_id}"
        update_data = {"properties": {"Status": {"select": {"name": "Опубликовано"}}}}
        data = json.dumps(update_data)
        requests.request("PATCH", update_url, headers=HEADERS, data=data)

    def public_messages(self, message_list):
        now = datetime.now(pytz.utc)
        cnt = 0
        bot = NewsBot(TG_TOKEN, CHANNEL_ID)
        for _message in message_list:
            try:
                public_time = datetime.fromisoformat(_message["time"])
            except TypeError:
                logger.info(f"Invalid date in message: {_message['title']}")
                continue
            if public_time < now:
                tg_message = me.create_message(_message)
                if tg_message["photo"]:
                    asyncio.run(bot.send_photo(tg_message["text"], tg_message["photo"]))
                else:
                    asyncio.run(bot.send_message(tg_message["text"]))
                cnt += 1
                self.change_news_status(_message["id"])
        return cnt

    def update_news(self):
        notion_db = self.read_database()
        news = self.find_news(notion_db)
        cnt = self.public_messages(news)
        logger.info(f"{cnt} news loaded to tg")
