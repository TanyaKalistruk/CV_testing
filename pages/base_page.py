from pages.search_page import SearchPage


class BasePage:

    def __init__(self, driver):
        self.base_url = "https://www.google.com/"
        self.driver = driver
        self.search_page = SearchPage(driver)

    def go_to_google_search(self):
        """Opens page by url where tests will start."""
        self.driver.get(self.base_url)
