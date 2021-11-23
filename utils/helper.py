"""Helper methods for tests."""
import configparser
import os
import glob
import re
import sys

from pages.search_object_on_image import SearchObjectOnImage


def remove_search_results_files():
    """Removes all image files with results of searching object that were created on previous test run."""
    files = glob.glob('../search_results/*.png')
    for file in files:
        os.remove(file)


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


def get_current_test_name() -> str:
    """Returns running test name."""
    return os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]


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
    output = get_file_path('search_results', get_current_test_name())
    ob = SearchObjectOnImage(exp, actual, output)
    ob.search_obj_on_template()
    return len(ob.accepted_points) == 1


def get_base_url_config() -> str:
    """Get base url from config and return it."""
    config = configparser.ConfigParser()
    config.read('../configs/config.ini')
    return config['base_configs']['base_url']
