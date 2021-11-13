"""Helper methods for tests."""
import configparser
import os
import re
import sys

from utils.search_object_on_image import SearchObjectOnImage


def get_screenshot_name_by_address(address: str) -> str:
    """
    Converts address into filename.
    Example: Chernivtsi, Holovna 22 -> chernivtsi_holovna_22
    """
    pattern = re.compile(r"(\,)*\s+")
    return re.sub(pattern, "_", address.lower())


def get_file_path(package_name: str, file_name: str) -> str:
    """Returns related file path to image filename."""
    for path in sys.path:
        if path.endswith('CV_testing'):
            screen_path = os.path.sep.join([path, 'tests', package_name, f"{file_name}.png"])
            pages_path = os.path.sep.join([path, 'tests', 'pages'])
            break
    else:
        raise FileNotFoundError(f"No files {sys.path}")
    return os.path.relpath(screen_path, pages_path)


def verify_location(address: str):
    """
    Verifies location by passed address.
    Note: for this verification image file in png format
    that is expected to be present should be in 'test_data' package
    with name by pattern in get_screenshot_name_by_address() method.
    Actual data is made by the test and is saved to the 'test_screen' packed with the same name.
    """
    file_name = get_screenshot_name_by_address(address)
    actual = get_file_path('test_screen', file_name)
    exp = get_file_path('test_data', file_name)
    ob = SearchObjectOnImage(exp, actual)
    ob.search_obj_on_template()
    return len(ob.accepted_points) == 1


def get_base_url_config() -> str:
    """Get base url from config and return it."""
    config = configparser.ConfigParser()
    config.read('../configs/config.ini')
    return config['base_configs']['base_url']
