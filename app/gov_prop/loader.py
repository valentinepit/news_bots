import json
import logging

import requests

from .governance.loader import get_new_gov_topics
from .proposal.loader import ProposalNews

logger = logging.getLogger(__name__)

source_list_path = "gov_prop/sources.json"
sources = json.loads(open(source_list_path, "r").read())

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}


def get_news():
    new_topics = {}
    for name, source in sources.items():
        if "gov" in source:
            response = requests.get(f"{source[0]}/latest", headers=headers)
            new_topics[name] = get_new_gov_topics(response)
        elif "prop" in source:
            proposal = ProposalNews(source[0])
            new_topics[name] = proposal.get_new_proposals()
    return new_topics
