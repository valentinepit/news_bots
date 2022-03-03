import logging
from datetime import datetime, timedelta

import requests
from lxml import html

logger = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}

base_url = "https://hacked.slowmist.io/en/"
days_ago = 1


def get_new_topics():
    news = {}
    page = 1
    while True:
        url = f"{base_url}?c=&page={str(page)}"
        now = datetime.now().date()
        _response = requests.get(url, headers=headers)
        if _response.status_code == 200:
            root = html.fromstring(_response.text)
            topics = root.xpath("//div[@class='case-content']/ul/li")
            for topic in topics:
                header = topic.xpath(".//h3/text()")[0]
                date = topic.xpath(".//span[@class='time']")[0].text
                content = topic.xpath(".//p/text()")[0]
                data = topic.xpath(".//p/span/text()")
                amount_of_loss = data[0].strip()
                attack_method = data[1].strip()
                try:
                    created_at = datetime.strptime(date, "%Y-%m-%d").date()
                except ValueError:
                    created_at = datetime.strptime(date, "%d %B %Y").date()
                if now - created_at < timedelta(days=days_ago):
                    name = f"{created_at.strftime('%Y-%m-%d')} - {header}"
                    news[name] = {
                        "date": created_at.strftime("%Y-%m-%d"),
                        "header": header,
                        "About (slowmist)": content,
                        "amount_of_loss": amount_of_loss,
                        "attack_method": attack_method,
                        "chain": "Unknown",
                        "source": url,
                        "About (defiyield.app)": "",
                    }
                else:
                    logger.info(f"{len(news)} added from {_response.url}")
                    return news
        page += 1
