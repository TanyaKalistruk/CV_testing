from selenium.webdriver.common.keys import Keys

from pages.driver_wrapper import Wrapper

SEARCH_INP_CSS = "input.gsfi"
SEARCH_BTH_CSS = ".FPdoLc .gNO89b"
ELEMENTS_IN_SEARCH_CSS = ".yuRUbf > a"


class SearchPage(Wrapper):
    """Class with methods for Search Google Page."""

    def __init__(self, driver):
        super().__init__(driver)

    def write_in_search_field(self, search_request: str):
        """Writes search request to input."""
        self.find_element_by_css(SEARCH_INP_CSS).send_keys(search_request)

    def send_search_request(self):
        """Clicks on Search button."""
        self.find_element_by_css(SEARCH_INP_CSS).send_keys(Keys.ENTER)

    def click_on_search_result_by_text(self, text: str):
        """Clicks on button by text."""
        elements = self.find_elements_by_css(ELEMENTS_IN_SEARCH_CSS)
        for element in elements:
            if text in element.text:
                element.click()
                break
        else:
            raise ()
