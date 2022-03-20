import logging
from datetime import datetime, timedelta

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.selen_driver import get_webdriver

logger = logging.getLogger(__name__)

url = "https://defiyield.app/rekt-database"
days_ago = 15
now = datetime.now().date()


def get_new_topics():
    news = {}
    driver = get_webdriver()
    try:
        driver.implicitly_wait(30)
        driver.get(url)
        last_message_date = now
        date_column = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='column date clickable']"))
        )
        date_column.click()
        while now - last_message_date < timedelta(days=days_ago):
            topics, last_message_date = get_page_topics(driver)
            news = {**news, **topics}
            pagination(driver)
    finally:
        driver.quit()
    logger.info(f"{len(news)} added from {url}")
    return news


def get_page_topics(driver):
    _news = {}
    created_at = now - timedelta(days=days_ago)
    WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='column date clickable']"))
    )
    logger.info(f"get a page with {url}")
    show_down = driver.find_elements(By.XPATH, ".//div[@class='column actions']")

    for button in show_down:
        try:
            button.click()
        except WebDriverException:
            continue
    topics = driver.find_elements(By.XPATH, "//div[@class='scam-database-row ']")
    for topic in topics:
        new_topic, created_at = topic_parser(topic)
        if not new_topic:
            break
        _news = {**_news, **new_topic}
    return _news, created_at


def topic_parser(_topic):
    new_topic = {}
    classes = {
        "chain": ".//div[@class='column tokens with-extra-info network']",
        "attack_method": ".//div[@class='column with-extra-info column-rekt-function']",
        "amount_of_loss": ".//div[@class='column funds-lost']",
        "About (defiyield.app)": ".//div[@class='description']",
    }
    date = _topic.find_element(By.XPATH, ".//div[@class='column date']").text
    created_at = datetime.strptime(date, "%d.%m.%Y").date()
    if now - created_at < timedelta(days=days_ago):
        header = _topic.find_element(By.XPATH, ".//div[@class='column justify-start project-name']").text.replace(
            " (2)", ""
        )
        name = f"{created_at.strftime('%Y-%m-%d')} - {header}"
        new_topic[name] = {
            "date": created_at.strftime("%Y-%m-%d"),
            "header": header,
            "source": url,
            "About (slowmist)": "",
        }
        for key, value in classes.items():
            try:
                elem = _topic.find_element(By.XPATH, value).text
            except NoSuchElementException:
                elem = ""
            new_topic[name][key] = elem
    else:
        new_topic = None

    return new_topic, created_at


def pagination(driver):
    next_button = driver.find_element(By.XPATH, "//div[@class='arrow right ']")
    next_button.click()
