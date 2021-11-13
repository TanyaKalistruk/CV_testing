from pages.map_page import MapPage
from pages.search_page import SearchPage


class BasePage:
    """BasePage for initiation other pages and easy access from the test."""

    def __init__(self, driver, base_url: str):
        self.base_url = base_url
        self.driver = driver
        self.search_page = SearchPage(driver)
        self.map_page = MapPage(driver)

    def go_to_google_search(self):
        """Opens page by url where tests will start."""
        self.driver.get(self.base_url)
