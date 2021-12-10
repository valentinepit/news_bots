import json
from datetime import datetime
import logging
import pytz
import requests
import asyncio
import message_editor as me
# import tg_bot.news_bot as nb
from tg_bot.aio_bot import NewsBot


logging.basicConfig(level=logging.INFO)
notion_token = "secret_c4oPq1SlK0KqW7sVTDIZf9sMcUEfua3Nr4ju2ebbF9T"

DB_ID = "9404aafb375a4132b9a10d069a2ac580"

HEADERS = {
    "Authorization": "Bearer " + notion_token,
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json",
}

TABLE_ROWS = ["Status",
              "Date to publish",
              "Name",
              "Notes",
              "Source",
              "#",
              "Addition"
              ]


def read_database():
    url = f"https://api.notion.com/v1/databases/{DB_ID}/query"
    res = requests.request("POST", url, headers=HEADERS)
    data = res.json()
    return data


def find_news(_data):
    public_list = []
    for item in _data["results"]:
        if item["properties"][TABLE_ROWS[0]]["select"]:
            if item["properties"]["Status"]["select"]["name"] == "Опубликовать":
                _news = me.convert_row_news(item["properties"])
                _news["id"] = item["id"]
                public_list.append(_news)
        else:
            continue
    return public_list


def change_news_status(page_id):
    update_url = f"https://api.notion.com/v1/pages/{page_id}"
    update_data = {
        "properties": {
            "Status": {
                "select": {
                    "name": "Опубликовано"
                }
            }
        }
    }
    data = json.dumps(update_data)
    response = requests.request("PATCH", update_url, headers=HEADERS, data=data)
    print(response.text)


def public_messages(message_list):
    now = datetime.now(pytz.utc)

    for _message in message_list:
        public_time = datetime.fromisoformat(_message['time'])
        if public_time < now:
            tg_message = me.create_message(_message)
            bot = NewsBot()
            asyncio.run(bot.send_message(tg_message))
            change_news_status(_message["id"])


notion_db = read_database()
news = find_news(notion_db)
public_messages(news)
