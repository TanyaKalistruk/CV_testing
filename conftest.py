import pytest
from selenium import webdriver

from constants.search_request_constants import GOOGLE_MAPS
from pages.base_page import BasePage


@pytest.fixture(scope="session")
def app():
    driver = webdriver.Chrome(r"C:\Users\Asus\Desktop\CV_testing\chromedriver.exe")
    return BasePage(driver)


@pytest.fixture(scope="session")
def app_maps(app):
    app.go_to_google_search()
    app.search_page.write_in_search_field(GOOGLE_MAPS)
    app.search_page.click_search_bth()
    app.search_page.click_on_search_result_by_text(GOOGLE_MAPS)
    return app
