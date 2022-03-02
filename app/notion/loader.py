import json
import logging
import os
from datetime import datetime

import pytz

import notion.message_editor as me
from contrib.notion.api import NotionAPI as na

logger = logging.getLogger(__name__)

NEWS_ID = os.environ["BASE_ID"]
FILTER = json.dumps({"filter": {"property": "Status", "select": {"equals": "тест"}}})


class News:
    def find_news(self, _data):
        public_list = []
        for item in _data["results"]:
            _news = me.convert_row_news(item["properties"])
            _news["id"] = item["id"]
            public_list.append(_news)
        return public_list

    def public_messages(self, message_list, api):
        now = datetime.now(pytz.utc)
        messages = []
        for _message in message_list:
            try:
                public_time = datetime.fromisoformat(_message["time"])
                if public_time < now:
                    tg_message = me.create_message(_message)
                    messages.append(tg_message)
                    api.change_news_status(_message["id"])
            except TypeError:
                logger.info(f"Invalid date in message: {_message['title']}")
                continue
        return messages

    def update_news(self):
        api = na()
        notion_db = api.read_database(NEWS_ID, FILTER)
        news = self.find_news(notion_db)
        messages = self.public_messages(news, api)
        logger.info(f"{len(messages)} news loaded to tg from Notion")
        return messages
