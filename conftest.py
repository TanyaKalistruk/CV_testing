import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from constants.search_request_constants import GOOGLE_MAPS
from pages.base_page import BasePage
from utils.helper import get_base_url_config


@pytest.fixture(scope="session")
def app():
    """Fixture with session scope that initiates BasePage."""
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_size(1490, 690)
    base_url = get_base_url_config()
    return BasePage(driver, base_url)


@pytest.fixture(scope="session")
def app_maps(app):
    """Fixture with session scope that opens Google Maps page."""
    app.go_to_google_search()
    app.search_page.write_in_search_field(GOOGLE_MAPS)
    app.search_page.send_search_request()
    app.search_page.click_on_search_result_by_text(GOOGLE_MAPS)
    return app
