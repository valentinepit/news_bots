import logging
from time import sleep

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from utils.selen_driver import get_webdriver

logger = logging.getLogger(__name__)


class ProposalNews:
    def __init__(self, url):
        self.url = url
        self.session_id = None

    def get_new_proposals(self):
        driver = get_webdriver()
        try:
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
        finally:
            driver.quit()
        return new_proposals

    def get_page(self, driver):
        if driver:
            driver.get(self.url)
            driver.implicitly_wait(30)
        return driver
