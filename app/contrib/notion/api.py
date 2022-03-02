import json
import logging
import os

import cfscrape
import requests
import requests.adapters
from requests.packages.urllib3.util.retry import Retry

from notion.message_editor import create_exploit_page, create_project_page

logger = logging.getLogger(__name__)


class NotionAPI:
    __API_URL_BASE = "https://api.notion.com/v1/"

    def __init__(self, api_base_url=__API_URL_BASE, request_timeout=120, proxy=None):
        self.api_base_url = api_base_url
        self.request_timeout = request_timeout

        self.session = cfscrape.CloudflareScraper()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries=retries))
        self.session.headers.update(
            {
                "Authorization": "Bearer " + os.environ["NOTION_TOKEN"],
                "Notion-Version": "2021-08-16",
                "Content-Type": "application/json",
            }
        )

    def __request(self, url, params):
        try:
            data = params["data"]
        except KeyError:
            data = None
        try:
            js = params["json"]
        except KeyError:
            js = None
        if url.endswith("query") or url.endswith("pages/"):
            response = self.session.post(url, timeout=self.request_timeout, data=data, json=js)
        else:
            response = self.session.patch(url, timeout=self.request_timeout, data=data, json=js)
        try:
            response.raise_for_status()
            return response.json()
        except Exception:
            # Raise exception with error from json
            try:
                content = json.loads(response.content.decode("utf-8"))
                raise ValueError(content)
            except json.decoder.JSONDecodeError:  # if no json
                pass
            raise

    def read_database(self, *args):
        _id = args[0]
        url = f"{self.__API_URL_BASE}databases/{_id}/query"
        return self.__request(url, {"data": args[1]})

    def create_page(self, *args):
        url = f"{self.__API_URL_BASE}pages/"

        if args[0] == "new_project":
            payload = create_project_page(args[1])
        else:
            payload = create_exploit_page(args[0], args[1])
        return self.__request(url, {"json": payload})["id"]

    def change_news_status(self, *args):
        page_id = args[0]
        url = f"{self.__API_URL_BASE}pages/{page_id}"
        update_data = {"properties": {"Status": {"select": {"name": "Опубликовано"}}}}
        data = json.dumps(update_data)
        return self.__request(url, {"data": data})
