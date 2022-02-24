import json
import logging
from typing import Dict

from app.contrib.notion import api as notion_api

from defiyield import get_new_topics as defiyeld
from hacked import get_new_topics as hacked

from app.notion import notion_app as nt

logger = logging.getLogger(__name__)

exploits_url = "https://www.notion.so/warpis/1dff0122648d4ec18133a1bbc15be575?v=a8c1c56de96e4d68a34816f8a9970ba1"

n = '2022-02-21 - Raptor2'
p = {'date': '2022-02-02', 'header': 'Raptor2',
     'About (defiyield.app)': "The contract deployer added initial liquidity at:\nhttps://bscscan.com/tx/0x78e7b5eb4d40ede331f2393db773ab62bbde2d936785c3eec77f0453232af9d4\n\nThe liquidity was removed and tokens were sold by the contract deployer:\nhttps://bscscan.com/tx/0xfbceeb8cb13a87e20ae0a1df2b8be0ff8f284f733ebacf4bd5c106f8b8c585f7\n\nStolen funds were transferred to the external address:\nhttps://bscscan.com/tx/0xef06c291b5f527d76643d9eb815dadff55b9ebf5b5320dd8faebc2684386bd5d\n\nThe funds' recipient deposited stolen funds into Tornado Cash Mixer:\nhttps://bscscan.com/address/0xdaa5e5692f24b0284cbd9fb6fbe2ddc78bf4d34a",
     'amount_of_loss': '$83,960', 'attack_method': 'Exit Scam', 'chain': 'BSC',
     'source': 'https://defiyield.app/rekt-database', 'About (slowmist)': ''}


def update_exploits():
    defiyeld_topics = defiyeld()
    hacked_topics = hacked()
    news = compile_topics(defiyeld_topics, hacked_topics)
    send_exploits_to_notion(news)


def send_exploits_to_notion(_data: Dict):
    for name, content in _data.items():
        content["projects"], content["blockchain"] = get_relations_id(content["header"])
        notion_api.create_page(name, content)


def compile_topics(main_list: Dict, secondary_list: Dict) -> Dict:
    two_sources_flag = False
    for secondary_name, _data in secondary_list.items():
        for main_topic in main_list.keys():
            if _data["header"] in main_topic:
                main_list[main_topic]['source'] += f", {_data['source']}"
                main_list[main_topic]['About (slowmist)'] = _data['About (slowmist)']
                two_sources_flag = True
                break
        if not two_sources_flag:
            main_list[secondary_name] = _data
        two_sources_flag = False
    return main_list


def get_relations_id(prj_name):
    chain_relations = []
    project_relations = []
    project_page_id = "b28af33c967d4f46873fe3ced821d5ac"
    _filter = json.dumps(
        {
            "filter":
                {"or": [
                    {"property": "Name", "text": {"equals": prj_name.split()[0]}},
                    {"property": "Name", "text": {"contains": prj_name}}
                ]
                }
        }
    )
    project_pages = notion_api.read_database(project_page_id, _filter)
    for page in project_pages["results"]:
        project_relations.append({"id": page["id"]})
        if page["properties"]["Chain"]["relation"]:
            chain_relations[0]["id"].append({"id": page["properties"]["Chain"]["relation"]})
    return project_relations, chain_relations


#
# get_relations_id(p["header"])
# notion_api.create_page(n, p)
update_exploits()
# # get_page()
# notion_api.read_database()
