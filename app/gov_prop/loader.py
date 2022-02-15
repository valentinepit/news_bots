import json

import requests

source_list_path = "app/gov_prop/sources.json"
sources = json.loads(open(source_list_path, "r").read())

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}


class GovernanceAndProposals:
    def get_new_gov_topics(self, _response):
        pass

    def get_new_prop_topics(self, _response):
        pass

    def send_news_to_tg(self, _messages):
        pass

    def get_news(self):
        new_topics = []
        for name, source in sources:
            if "gov" in source:
                response = requests.get(f"{source[0]}/latest", headers=headers)
                new_topics.append(self.get_new_gov_topics(response))
            elif "prop" in source:
                response = requests.get(f"{source[0]}/#/", headers=headers)
                new_topics.append(self.get_new_prop_topics(response))
