import allure
from constants.address_constants import CHERNIVTSI_HOLOVNA_22, CHERNIVTSI_KOTSYBYNSKOGO_2, CHERNIVTSI_HOLOVNA_87, \
    CHERNIVTSI_UNIVERSITETSKA_10
from constants.search_request_constants import GOOGLE_MAPS
from utils.helper import verify_location


def test_search_holovna_address(app_maps):
    """Verify that expected location is selected for Chernivtsi, Holovna 22 address."""
    # bad screenshot
    with allure.step("Zoom the map."):
        app_maps.map_page.zoom_btn_click()
    with allure.step("Search the address"):
        app_maps.map_page.search_the_address(CHERNIVTSI_HOLOVNA_22)
        app_maps.map_page.wait()
        assert app_maps.map_page.is_information_panel_present()
    with allure.step(f"Verify {CHERNIVTSI_HOLOVNA_22} address is located on the map"):
        app_maps.map_page.get_screen(CHERNIVTSI_HOLOVNA_22)
        assert verify_location(CHERNIVTSI_HOLOVNA_22)


def test_search_kotsybynskogo_address(app_maps):
    """Verify that expected location is selected for Chernivtsi, Kotsyubynskogo 2 address."""
    # positive
    with allure.step("Zoom the map."):
        app_maps.map_page.zoom_btn_click()
    with allure.step("Search the address"):
        app_maps.map_page.search_the_address(CHERNIVTSI_KOTSYBYNSKOGO_2)
        app_maps.map_page.wait()
        assert app_maps.map_page.is_information_panel_present()
    with allure.step(f"Verify {CHERNIVTSI_KOTSYBYNSKOGO_2} address is located on the map"):
        app_maps.map_page.get_screen(CHERNIVTSI_KOTSYBYNSKOGO_2)
        assert verify_location(CHERNIVTSI_KOTSYBYNSKOGO_2)


def test_click_unexist_bth(app):
    """Negative test for sending data by not existing selector."""
    # fail
    with allure.step("Search Google Maps."):
        app.go_to_google_search()
        app.search_page.write_in_search_field(GOOGLE_MAPS)
        app.search_page.send_search_request_unexist_field()


def test_search_holovna_87_address(app_maps):
    """Verify that expected location is selected for Chernivtsi, Holovna 87 address."""
    with allure.step("Zoom the map."):
        app_maps.map_page.zoom_btn_click()
    with allure.step("Search the address"):
        app_maps.map_page.search_the_address(CHERNIVTSI_HOLOVNA_87)
        app_maps.map_page.wait()
        assert app_maps.map_page.is_information_panel_present()
    with allure.step(f"Verify {CHERNIVTSI_HOLOVNA_87} address is located on the map"):
        app_maps.map_page.get_screen(CHERNIVTSI_HOLOVNA_87)
        assert verify_location(CHERNIVTSI_HOLOVNA_87)


def test_search_universitetska_address(app_maps):
    """Verify that expected location is selected for Chernivtsi, Universitetska 10 address."""
    with allure.step("Zoom the map."):
        app_maps.map_page.zoom_btn_click()
    with allure.step("Search the address"):
        app_maps.map_page.search_the_address(CHERNIVTSI_UNIVERSITETSKA_10)
        app_maps.map_page.wait()
        assert app_maps.map_page.is_information_panel_present()
    with allure.step(f"Verify {CHERNIVTSI_UNIVERSITETSKA_10} address is located on the map"):
        app_maps.map_page.get_screen(CHERNIVTSI_UNIVERSITETSKA_10)
        assert verify_location(CHERNIVTSI_UNIVERSITETSKA_10)
