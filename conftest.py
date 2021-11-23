import glob
import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from constants.search_request_constants import GOOGLE_MAPS
from pages.base_page import BasePage
from utils.helper import get_base_url_config, remove_search_results_files


@pytest.fixture(scope="function")
def app():
    """Fixture with session scope that initiates BasePage."""
    driver = webdriver.Chrome(r"C:\Users\Asus\Desktop\CV_testing\chromedriver.exe")
    driver.set_window_size(1490, 690)
    base_url = get_base_url_config()
    remove_search_results_files()
    yield BasePage(driver, base_url)
    driver.close()


@pytest.fixture(scope="function")
def app_maps(app):
    """Fixture with session scope that opens Google Maps page."""
    app.go_to_google_search()
    app.search_page.write_in_search_field(GOOGLE_MAPS)
    app.search_page.send_search_request()
    app.search_page.click_on_search_result_by_text(GOOGLE_MAPS)
    return app


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Hook the "item" object on a test failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot(request, app):
    """Make screenshot on a test failure."""
    yield
    make_screenshot(app.driver, request.function.__name__)


def make_screenshot(driver, function_name: str):
    """Method for making a screenshot."""
    files = glob.glob(f'../search_results/{function_name}.png')
    if len(files) == 0:
        allure.attach(driver.get_screenshot_as_png(),
                      name=function_name,
                      attachment_type=AttachmentType.PNG)
    else:
        with open(files[0], "rb") as image:
            f = image.read()
            b = bytearray(f)
            allure.attach(b,
                          name=function_name,
                          attachment_type=AttachmentType.PNG)

