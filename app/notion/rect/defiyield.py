import logging
from datetime import datetime, timedelta

from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

url = "https://defiyield.app/rekt-database"
days_ago = 10


def get_webdriver():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x935")
        options.add_argument("--kiosk")
        options.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=options)

    except WebDriverException as e:
        logger.info(f"Can't get webdriver: {e}")
        return
    return driver


def get_new_topics():
    news = []
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

        for topic in topics:
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
                news.append([date, header, content, amount_of_loss, attack_method, chain])
    finally:
        driver.quit()
    logger.info(f"{len(news)} added from {url}")
    return news

