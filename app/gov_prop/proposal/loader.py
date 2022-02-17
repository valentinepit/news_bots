import logging
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class ProposalNews:
    def __init__(self, url):
        self.url = url

    def get_webdriver(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            options.add_argument("window-size=1920x935")
            options.add_argument("--kiosk")
            options.add_argument("--log-path=proposal.log")
            options.add_argument("--log-level=3")
            driver = webdriver.Chrome(options=options)
        except WebDriverException as e:
            logger.info(f"Can't get webdriver: {e}")
            return
        return driver

    def get_new_proposals(self):
        driver = self.get_webdriver()
        page = self.get_page(driver)
        new_proposals = []
        status = ""
        while status != "Closed":
            sleep(2)
            containers = page.find_elements(By.XPATH, "//div[@class='leading-6']")
            for container in containers[1:]:
                try:
                    status = container.find_element(By.CLASS_NAME, "State").text
                except StaleElementReferenceException:
                    continue
                if status != "Closed":
                    try:
                        text = container.find_element(By.CLASS_NAME, "break-words").text
                    except StaleElementReferenceException:
                        text = ""
                    try:
                        header = container.find_element(By.CLASS_NAME, "my-1").text
                    except StaleElementReferenceException:
                        continue
                    msg = f"{header}\n{text}"
                    if msg not in new_proposals:
                        new_proposals.append(msg)
            page.execute_script("window.scrollTo(0, window.scrollY + 200)")
        logger.info(f"{len(new_proposals)} added from {self.url}")
        return new_proposals

    def get_page(self, driver):
        if driver:
            driver.get(self.url)
            driver.implicitly_wait(30)
        return driver
