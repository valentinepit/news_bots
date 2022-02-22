import logging

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities

logger = logging.getLogger(__name__)


def get_webdriver():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x935")
        options.add_argument("--kiosk")
        options.add_argument("--log-level=3")
        driver = webdriver.Remote(
            command_executor="http://chromedriver:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options,
        )
    except WebDriverException as e:
        logger.info(f"Can't get webdriver: {e}")
        return
    return driver
