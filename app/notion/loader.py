import logging
import os
from datetime import datetime

import pytz

import app.notion.message_editor as me
from app.contrib.notion import api as notion_api

logger = logging.getLogger(__name__)


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

