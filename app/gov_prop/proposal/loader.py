import logging

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.selen_driver import get_webdriver

logger = logging.getLogger(__name__)


class ProposalNews:
    def __init__(self, url):
        self.url = url

    def get_new_proposals(self):
        driver = get_webdriver()
        driver.implicitly_wait(150)
        try:
            page = self.get_page(driver)
            new_proposals = []
            status = ""
            while status != "Closed":
                wait = WebDriverWait(driver, 100)
                wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='truncate w-full']")))
                containers = page.find_elements(By.XPATH, "//div[@class='leading-5 sm:leading-6']")
                for container in containers[1:]:
                    try:
                        status = container.find_element(By.CLASS_NAME, "State").text
                    except (NoSuchElementException, StaleElementReferenceException):
                        continue
                    if status != "Closed" or status == "":
                        try:
                            text = container.find_element(By.XPATH, "//p[@class='break-words mb-2 sm:text-md']").text
                        except NoSuchElementException:
                            text = ""
                        try:
                            header = container.find_element(By.CLASS_NAME, "my-1").text
                        except NoSuchElementException:
                            continue
                        msg = f"<b>{header}</b>\n{text}"
                        if msg not in new_proposals:
                            new_proposals.append(msg)
                    else:
                        break
                    page.execute_script("window.scrollTo(0, window.scrollY + 200)")
        finally:
            driver.quit()
        return new_proposals

    def get_page(self, driver):
        if driver:
            driver.get(self.url)
            driver.implicitly_wait(30)
        return driver
