from constants.address_constants import CHERNIVTSI_HOLOVNA_22
from utils.helper import verify_location


def test_search_holovna_address(app_maps):
    """Verify that expected location is selected for Chernivtsi, Holovna 22 address."""
    app_maps.map_page.zoom_btn_click()
    app_maps.map_page.search_the_address(CHERNIVTSI_HOLOVNA_22)
    app_maps.map_page.wait()
    assert app_maps.map_page.is_information_panel_present()
    app_maps.map_page.get_screen(CHERNIVTSI_HOLOVNA_22)
    assert verify_location(CHERNIVTSI_HOLOVNA_22)
