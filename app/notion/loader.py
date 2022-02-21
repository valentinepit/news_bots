import json
import logging
import os
from datetime import datetime
from app.contrib.notion import api as notion_api

import pytz
import requests

import app.notion.message_editor as me

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
    def find_news(self, _data):
        public_list = []
        for item in _data["results"]:
            _news = me.convert_row_news(item["properties"])
            _news["id"] = item["id"]
            public_list.append(_news)
        return public_list

    def public_messages(self, message_list):
        now = datetime.now(pytz.utc)
        messages = []
        for _message in message_list:
            try:
                public_time = datetime.fromisoformat(_message["time"])
            except TypeError:
                logger.info(f"Invalid date in message: {_message['title']}")
                continue
            if public_time < now:
                tg_message = me.create_message(_message)
                messages.append(tg_message)
                notion_api.change_news_status(_message["id"])
        return messages

    def update_news(self):
        notion_db = notion_api.read_database()
        news = self.find_news(notion_db)
        messages = self.public_messages(news)
        logger.info(f"{len(messages)} news loaded to tg from Notion")
        return messages

