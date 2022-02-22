import logging
from typing import Dict, List

from contrib.notion import api as notion_api

from .defiyield import get_new_topics as defiyeld
from .hacked import get_new_topics as hacked

logger = logging.getLogger(__name__)


def update_exploits():
    defiyeld_topics = defiyeld()
    hacked_topics = hacked()
    news = compile_topics(defiyeld_topics, hacked_topics)
    for item in news:
        send_exploits_to_notion(item)


def send_exploits_to_notion(_data: Dict):
    for name, content in _data.items():
        notion_api.create_page(name, content)


def compile_topics(main_list: Dict, secondary_list: Dict) -> Dict:

    for name, _data in secondary_list.items():
        if name not in main_list:
            main_list[name] = _data
        else:
            main_list[name]['source'] += f", {_data['source']}"
            main_list[name]['slowmist'] = _data['content']
    return main_list

update_exploits()