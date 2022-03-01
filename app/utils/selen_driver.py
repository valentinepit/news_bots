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
    driver.request_interceptor = interceptor
    return driver


def interceptor(request):
    del request.headers["Referer"]
    request.headers["Referer"] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
