import pytest
from base.webdriverfactory import WebDriverFactory

@pytest.fixture()
def setUp():
    print("Starting test case")
    yield
    print("Finishing up test case")

@pytest.fixture(scope = 'class')
def oneTimeSetUp(request, browser):
    print("One time setUp of a test run")
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()
    print("One time tearDown of a test run")

def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--osType", help="Type of operating system")

@pytest.fixture(scope = "session")
def browser(request):
    return request.config.getoption("--browser")
