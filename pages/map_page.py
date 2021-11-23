from selenium.webdriver.common.keys import Keys

from pages.driver_wrapper import Wrapper
from utils.helper import get_screenshot_name_by_address, get_file_path

ZOOM_BTN_CSS = "#widget-zoom-in"
INFORMATION_PANEL_CSS = "#pane .Yr7JMd-pane-content"
SEARCH_FIELD_CSS = "#searchboxinput"


class MapPage(Wrapper):

    def __init__(self, driver):
        super().__init__(driver)

    def zoom_btn_click(self, click_count: int = 4):
        """Clicks on zoom button click_count times."""
        zoom_btn_element = self.find_element_by_css(ZOOM_BTN_CSS)
        for _ in range(click_count):
            zoom_btn_element.click()

    def zoom_btn_unexist_click(self, click_count: int = 4):
        """Clicks on zoom button click_count times."""
        zoom_btn_element = self.find_element_by_css("unexist")
        for _ in range(click_count):
            zoom_btn_element.click()

    def search_the_address(self, address: str):
        """Clicks on zoom button click_count times."""
        search_field_element = self.find_element_by_css(SEARCH_FIELD_CSS)
        search_field_element.click()
        search_field_element.send_keys(address)
        search_field_element.send_keys(Keys.ENTER)

    def is_information_panel_present(self, timeout: int = 5) -> bool:
        """Returns is information panel about specified address present or not."""
        return self.find_element_by_css(INFORMATION_PANEL_CSS, timeout).is_displayed()

    def get_screen(self, address: str):
        """Makes screenshot of map and save it into 'test_screen' package with address as file name."""
        file_name = get_screenshot_name_by_address(address)
        self.driver.save_screenshot(get_file_path('test_screen', file_name))
