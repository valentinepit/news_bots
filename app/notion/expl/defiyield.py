import logging
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.selen_driver import get_webdriver

logger = logging.getLogger(__name__)

url = "https://defiyield.app/rekt-database"
days_ago = 1


def get_new_topics():
    news = {}
    now = datetime.now().date()
    driver = get_webdriver()
    driver.implicitly_wait(30)
    driver.get(url)
    try:
        date_column = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='column date clickable']"))
        )
        date_column.click()
        show_down = driver.find_elements(By.XPATH, ".//div[@class='column actions']")
        for button in show_down:
            button.click()
        topics = driver.find_elements(By.XPATH, "//div[@class='scam-database-row ']")

        for en, topic in enumerate(topics):
            news_headers = topic.text.split("\n")
            header, chain, attack_method, amount_of_loss, date = (
                news_headers[0],
                news_headers[1],
                news_headers[2],
                news_headers[3],
                news_headers[4],
            )
            content = topic.find_element(By.XPATH, ".//div[@class='description']").text
            try:
                created_at = datetime.strptime(date, "%d.%m.%Y").date()
            except ValueError:
                attack_method, amount_of_loss, date = news_headers[3], news_headers[4], news_headers[5]
                created_at = datetime.strptime(date, "%d.%m.%Y").date()
            if now - created_at < timedelta(days=days_ago):
                name = f"{url}_{en}"
                news[name] = {
                    "date": created_at.strftime("%Y-%m-%d"),
                    "header": header,
                    "content": content,
                    "amount_of_loss": amount_of_loss,
                    "attack_method": attack_method,
                    "chain": chain,
                }
    finally:
        driver.quit()
    logger.info(f"{len(news)} added from {url}")
    return news
