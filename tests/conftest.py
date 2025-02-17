import os
import sys
import base64
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Utilities.configurations import getConfig


@pytest.fixture(scope="session")
def setup(browser):
    driver = get_driver(browser)

    if driver:
        print(f"Launching {browser} Browser")
    else:
        print(f"Invalid browser name {browser} provided")

    yield driver

    # Close the driver after test session ends
    if driver:
        print(f"Closing {browser} Browser")
        driver.quit()


def get_driver(browser):
    if browser == "chrome":
        chrome_driver_path = "C:\\Drivers\\chromedriver.exe"
        options = webdriver.ChromeOptions()
        serv_obj = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=serv_obj, options=options)
        return driver
    else:
        return None


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope='session')
def api_headers():
    config = getConfig()
    merchantid = config['API']['merchantID']
    username = config['API']['apiKey']
    password = ""
    credentials = f"{username}:{password}".encode("utf-8")
    base64_credentials = base64.b64encode(credentials).decode("utf-8")
    headers = {
        "merchantid": f"{merchantid}",
        "Content-Type": "application/json",
        "Authorization": f"Basic {base64_credentials}"
    }
    return headers


# Configure reports with timestamp and create reports directory if it doesn't exist
@pytest.hookimpl(optionalhook=True)
def pytest_configure(config):
    import os
    from datetime import datetime

    # Get the test file name from the command-line arguments
    if config.args:
        test_file_name = os.path.splitext(os.path.basename(config.args[0]))[0]
    else:
        test_file_name = "test_report"  # Default name if no specific file is passed

    report_dir = os.path.abspath(os.curdir) + "\\reports\\"
    os.makedirs(report_dir, exist_ok=True)

    # Generate the report filename with timestamp
    report_filename = f"{test_file_name} - {datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.html"

    # Ensure the HTML report path is set correctly
    html_path = os.path.join(report_dir, report_filename)
    config.option.htmlpath = html_path
