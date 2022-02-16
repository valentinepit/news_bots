import json
from datetime import datetime, timedelta

import requests
from lxml import html

source_list_path = "app/gov_prop/sources.json"
sources = json.loads(open(source_list_path, "r").read())

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}


class GovernanceAndProposals:
    def get_new_gov_topics(self, _response):
        news = []
        now = datetime.now().date()
        if _response.status_code == 200:
            root = html.fromstring(_response.text)
            topics = root.xpath("//tr[@class='topic-list-item']")
            for topic in topics:
                header = topic.xpath(".//a[@class='title raw-link raw-topic-link']/text()")[0]
                date = topic.xpath(".//td[last()]/text()")[0].strip()
                try:
                    created_at = datetime.strptime(date, "%B %d, %Y").date()
                except ValueError:
                    created_at = datetime.strptime(date, "%d %B %Y").date()
                if now - created_at < timedelta(days=1):
                    news.append([header, created_at])
        return news

    def get_new_prop_topics(self, _response):
        news = []
        now = datetime.now().date()
        if _response.status_code == 200:
            root = html.fromstring(_response.text)
            topics = root.xpath("//div[@class='border-t border-b md:border rounded-none md:rounded-lg mb-4 bg-skin-block-bg timeline-proposal transition-colors']")


    def send_news_to_tg(self, _messages):
        pass

    def get_news(self):
        new_topics = {}
        for name, source in sources.items():
            if "gov" in source:
                response = requests.get(f"{source[0]}/latest", headers=headers)
                new_topics[name] = self.get_new_gov_topics(response)
            elif "prop" in source:
                response = requests.get(f"{source[0]}/#/", headers=headers)
                new_topics[name] = self.get_new_prop_topics(response)


def start():
    parser = GovernanceAndProposals()
    parser.get_news()
