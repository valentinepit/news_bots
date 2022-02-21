import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://api.notion.com/v1/"
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DB_ID = os.environ["BASE_ID"]
FILTER = json.dumps({"filter": {"property": "Status", "select": {"equals": "Опубликовать"}}})

HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json",
}


def read_database(self):
    url = f"{BASE_URL}databases/{DB_ID}/query"
    res = requests.request("POST", url, headers=HEADERS, data=FILTER)
    logger.info("We have logged in to Notion")
    data = res.json()
    return data

def change_news_status(self, page_id):
    update_url = f"{BASE_URL}pages/{page_id}"
    update_data = {"properties": {"Status": {"select": {"name": "Опубликовано"}}}}
    data = json.dumps(update_data)
    requests.request("PATCH", update_url, headers=HEADERS, data=data)
