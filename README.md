# CV_testing

This project was crated for demonstration of using computer vision for integration UI tests. There are added a few demo tests for Google Maps page.

Tests are written using Python3.7. During runs information is logged by `logging` lib and reports are served by `allure`.


### Installing requirements
1.  [install allure](https://docs.qameta.io/allure/) 
2. run `pip install -r requirements.pip` to install all other dependencies.
3. chromedriver will be installed automatically depending on your Chrome browser verion before tests running.


### Running integration tests
For running tests use this command `pytest tests/ --alluredir=reports/`.

For serving reports after test run use this command `allure serve tests/reports/`.


### Adding new tests
For adding new tests or modifying existing tests for new address you need:
1. Add .png file with any image that has size the same as you are going to take screenshots in tests into `CV_testing/test_screen`. Note: file name should be the same as your new address.
2. Add .png file with expected data (part of image) to `CV_testing/test_data`. Note: file name should be the same as your new address.
3. Go to `CV_tests/tests` and update of add a new test with your address.
4. Run it and enjoy!
