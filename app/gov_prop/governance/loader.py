import logging
from datetime import datetime, timedelta

from lxml import html

logger = logging.getLogger(__name__)


def get_new_gov_topics(_response):
    news = []
    now = datetime.now().date()
    if _response.status_code == 200:
        root = html.fromstring(_response.text)
        topics = root.xpath("//tr[@class='topic-list-item']")
        for topic in topics:
            header = topic.xpath(".//a[@class='title raw-link raw-topic-link']/text()")[0]
            link = _response.url + topic.xpath(".//a[@class='title raw-link raw-topic-link']")[0].get("href")
            date = topic.xpath(".//td[last()]/text()")[0].strip()
            try:
                created_at = datetime.strptime(date, "%B %d, %Y").date()
            except ValueError:
                created_at = datetime.strptime(date, "%d %B %Y").date()
            if now - created_at < timedelta(days=1):
                news.append(f"{header}\n{link}\n{date}")
            else:
                break
    logger.info(f"{len(news)} added from {_response.url}")
    return news
