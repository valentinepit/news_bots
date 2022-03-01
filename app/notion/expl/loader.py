import json
import logging
from typing import Dict

from contrib.notion import api as notion_api

from .defiyield import get_new_topics as defiyeld
from .hacked import get_new_topics as hacked

logger = logging.getLogger(__name__)


def update_exploits():
    defiyeld_topics = defiyeld()
    hacked_topics = hacked()
    news = compile_topics(defiyeld_topics, hacked_topics)
    send_exploits_to_notion(news)
    return len(news)


def send_exploits_to_notion(_data: Dict):
    for name, content in _data.items():
        content["projects"], content["blockchain"] = get_relations_id(content)
        if not content["projects"]:
            new_project_id = notion_api.create_page("new_project", content)
            content["projects"].append({"id": new_project_id})
        notion_api.create_page(name, content)


def compile_topics(main_list: Dict, secondary_list: Dict) -> Dict:
    two_sources_flag = False
    for secondary_name, _data in secondary_list.items():
        for main_name, main_data in main_list.items():
            two_sources_flag = check_inclusion(main_data, _data)
            if two_sources_flag:
                main_list[main_name]["source"] += f", {_data['source']}"
                main_list[main_name]["About (slowmist)"] = _data["About (slowmist)"]
                two_sources_flag = True
                break
        if not two_sources_flag:
            main_list[secondary_name] = _data
    return main_list


def check_inclusion(first: Dict, second: Dict) -> bool:
    name_1 = first["header"].lower()
    name_2 = second["header"].lower()
    if first["date"] == second["date"] or \
            (name_1 in name_2 or name_2 in name_1) or \
            name_1.split()[0] in name_2 or \
            name_1.replace(" ", "") in name_2 or \
            first["amount_of_loss"] == second["amount_of_loss"]:
        return True
    return False


def get_relations_id(_data):
    chain_relations = []
    project_relations = []
    project_page_id = "b28af33c967d4f46873fe3ced821d5ac"
    _filter = json.dumps(
        {
            "filter": {
                "or": [
                    {"property": "Name", "text": {"equals": _data["header"].split()[0]}},
                    {"property": "Name", "text": {"contains": _data["header"]}},
                ]
            }
        }
    )
    project_pages = notion_api.read_database(project_page_id, _filter)
    for page in project_pages["results"]:
        project_relations.append({"id": page["id"]})
        if page["properties"]["Chain"]["relation"]:
            chain_relations.append({"id": page["properties"]["Chain"]["relation"][0]["id"]})

    if not chain_relations:
        _filter = json.dumps({"filter": {"property": "Name", "text": {"equals": _data["chain"]}}})

        blockchain_page_id = "685ecddce4984e2da6b27f907497e51a"
        blockchain_pages = notion_api.read_database(blockchain_page_id, _filter)

        for page in blockchain_pages["results"]:
            chain_relations.append({"id": page["id"]})
    return project_relations, chain_relations

