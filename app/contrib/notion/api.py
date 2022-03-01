import json
import logging
import os

import requests

from notion.message_editor import create_exploit_page, create_project_page

logger = logging.getLogger(__name__)

BASE_URL = "https://api.notion.com/v1/"
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DB_ID = os.environ["BASE_ID"]

EXPLOITS_ID = os.environ["EXPLOITS_ID"]

FILTER = json.dumps({"filter": {"property": "Status", "select": {"equals": "Опубликовать"}}})

HEADERS = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json",
}


def read_database(_id=DB_ID, _filter=FILTER):
    url = f"{BASE_URL}databases/{_id}/query"
    res = requests.request("POST", url, headers=HEADERS, data=_filter)
    data = res.json()
    return data


def change_news_status(page_id):
    update_url = f"{BASE_URL}pages/{page_id}"
    update_data = {"properties": {"Status": {"select": {"name": "Опубликовано"}}}}
    data = json.dumps(update_data)
    requests.request("PATCH", update_url, headers=HEADERS, data=data)


def create_page(_source, _data):
    url = f"{BASE_URL}pages/"
    if _source == "new_project":
        payload = create_project_page(_data)
    else:
        payload = create_exploit_page(_source, _data)
    res = requests.request("POST", url, json=payload, headers=HEADERS)
    return res.json()["id"]
