import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from utils.logger import logger


class Wrapper:
    """Wrapper for Selenium WebDriver."""

    log = logger()

    def __init__(self, driver):
        self.driver = driver

    def find_element_by_css(self, selector: str, timeout: int = 10) -> WebElement:
        """Wait for element by passes selector being present and return it."""
        try:
            WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located((By.CSS_SELECTOR, selector)),
                                                      message=f"Can't find element by locator {selector}")
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            self.log.info(f"Element {selector} found successful")
            return element
        except TimeoutError:
            self.log.error(f"Element {selector} was not found during {timeout} timeout")
        except NoSuchElementException:
            self.log.error(f"Element {selector} not found")

    def find_elements_by_css(self, selector: str, timeout: int = 10) -> list:
        """Wait for element by passes selector being present and return it."""
        try:
            WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located((By.CSS_SELECTOR, selector)),
                                                      message=f"Can't find element by locator {selector}")
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            self.log.info(f"Element {selector} found successful")
            return elements
        except TimeoutError:
            self.log.error(f"Element {selector} was not found during {timeout} timeout")
        except NoSuchElementException:
            self.log.error(f"Element {selector} not found")

    def wait(self, timeout: int = 10):
        """Waits for time specified in timeout variable."""
        time.sleep(timeout)
