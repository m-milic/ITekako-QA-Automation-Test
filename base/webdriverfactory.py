"""
Creates a webdriver instance based on browser configurations
"""
from selenium import webdriver

class WebDriverFactory():

    def __init__(self, browser):
        self.browser = browser

    def getWebDriverInstance(self, baseURL="http://10.15.1.204:3000/"):
        """
        Get WebDriver Instance based on the browser configuration
        """

        if self.browser == "iexplorer":
            # Set ie driver
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            driver = webdriver.Firefox(executable_path=r"drivers/geckodriver.exe")
        elif self.browser == "chrome":
            # Set chrome driver
            driver = webdriver.Chrome(executable_path=r"drivers/chromedriver.exe")
        else:
            driver = webdriver.Firefox()

        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(3)
        # Maximize the window
        driver.maximize_window()
        # Loading browser with app URL
        driver.get(baseURL)
        return driver
