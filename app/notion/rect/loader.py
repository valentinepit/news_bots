import logging
from typing import Dict

from app.contrib.notion import api as notion_api
from defiyield import get_new_topics as defiyeld
from hacked import get_new_topics as hacked

logger = logging.getLogger(__name__)


def get_new_exploits():
    for news in [defiyeld(), hacked()]:
        send_exploits_to_notion(news)


def send_exploits_to_notion(_data: Dict):
    for name, content in _data.items():
        _source = name[: name.index("_")]
        notion_api.create_page(_source, content)


get_new_exploits()
