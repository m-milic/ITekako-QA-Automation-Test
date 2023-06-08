from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import utilities.custom_logger as cl
import logging
import time
import os


class SeleniumDriver:

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        """
        Takes screenshot of the current open web page
        """
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotsDirectory = "../screenshots/"
        relativeFileName = screenshotsDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotsDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot saved to location: " + destinationFile)
        except:
            self.log.error("### Exception Occurred")
            print_stack()

    def getTitle(self):
        """
        Gets title of the webpage.
        /// Not used in this test. ///
        """
        return self.driver.title

    def getByType(self, locatorType):
        """
        Tool for selecting By Type based on string inputed when getting/interacting with the element.
        """
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type is not supported")
        return False

    def getElement(self, locator, locatorType="xpath"):
        """
        Gets element by any locator type, based on inputed string.
        """
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element found with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Element not found with locator: " + locator + " locatorType: " + locatorType)
        return element

    def getElementList(self, locator, locatorType="xpath"):
        """
        Gets element list by any locator type, based on inputed string.
        """
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info("Element list found with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Element list not found with locator: " + locator + " locatorType: " + locatorType)
        return element

    def elementClick(self, locator="", locatorType="xpath", element=None):
        """
        Can either provide element, or element locator and locatorType
        """
        r = True
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on the element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            r = False
            print_stack()
        return r

    def sendKeys(self, data, locator="", locatorType="xpath", element=None):
        """
        Can either provide element, or element locator and locatorType
        """
        r = True
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("Sent data to the element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot send data to the element with locator: " + locator + " locatorType: " + locatorType)
            r = False
            print_stack()
        return r

    def typeKeys(self, data):
        """
        Types keys (to no specific element).
        """
        r = True
        try:
            actions = ActionChains(self.driver)
            actions.send_keys(data)
            actions.perform()
            self.log.info("Successfully typed keys: " + data)
        except:
            self.log.info("Cannot type keys: " + data)
            r = False
            print_stack()
        return r

    def sendEnter(self, locator="", locatorType="xpath", element=None):
        """
        Sends a common key to an element.
        Can either provide element, or element locator and locatorType
        """
        r = True
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.send_keys(Keys.ENTER)
            self.log.info("Sent Enter key to the element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot send Enter key to the element with locator: " + locator + " locatorType: " + locatorType)
            r = False
            print_stack()
        return r

    def selectFromDD(self, value, locator="", locatorType="xpath", element=None):
        """
        Selects an option from the dropdown.
        Can either provide element, or element locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.selectByValue(value)
            self.log.info("Selected option " + value + " on the element with locator " + locator
                          + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot select option " + value + " from the element with locator: "
                          + locator + " locatorType: " + locatorType)
            print_stack()

    def getText(self, locator="", locatorType="xpath", element=None, info=""):
        """
        Gets 'Text' from an element.
        Can either provide element, or element locator and locatorType
        info parameter is not functional, used only to describe the element we're getting text from
        """
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding text")
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) !=0:
                self.log.info("Getting text on element ::" + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def isElementPresent(self, locator="", locatorType="xpath", element=None):
        """
        /// Not used for this test ///
        Can either provide element, or element locator and locatorType
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False

    def isElementDisplayed(self, locator="", locatorType="xpath", element=None):
        """
        /// Not used for this test ///
        Can either provide element, or element locator and locatorType
        """
        isDisplayed=False
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                if isDisplayed:
                    self.log.info("Element is displayed, with locator: " + locator + " locatorType: " + locatorType)
                else:
                    self.log.info("Element is not displayed, with locator: " + locator + " locatorType: " + locatorType)
            else:
                self.log.info("Element not found, with locator: " + locator + " locatorType: " + locatorType)
            return isDisplayed
        except:
            print("Element not found")
            return False

    def waitForElement(self, locator, locatorType='xpath', timeout=10, pollFrequency=0.5):

        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) + ":: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((byType, locator)))
            self.log.info("Element appeared on the web page")

        except:
            self.log.info("Element has not appeared on the web page")
            print_stack()
        self.driver.implicit_wait(2)
        return element

    def clearField(self, locator="", locatorType='xpath', element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.clear()
            self.log.info("Cleared field of the element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot clear field of the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def clearInnerHtml(self, locator="", locatorType='xpath', element=None):
        """
        Clears innerText from element.
        Made to avoid refreshing page mid-test in Problem 2.
        Can either provide element, or element locator and locatorType
        """
        r = True
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding text")
            self.driver.execute_script("arguments[0].innerText = ''", element)
        except:
            self.log.error("Failed to remove text from the element " + element)
            print_stack()
            r = False
        return r

    def webScroll(self, direction="down"):
        """
        Scrolls by 1000 pixels
        Down is the default scroll direction
        /// Modification for this test was to scroll back up after going down, to avoid some button clicking problems///
        """
        if direction =="up":
            self.driver.execute_script("window.scrollBy(0, -1000);")
        if direction == "down":
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)
            self.driver.execute_script("window.scrollBy(0, -400);")

    def navigateBack(self):
        """
        /// Not used in this test ///
        """
        self.driver.back()

    def getLocalStorage(self):
        """
        Returns the local storage
        """
        a = None
        try:
            a = self.driver.execute_script("return window.localStorage;")
            self.log.info("Was able to fetch local storage")
        except:
            self.log.info("Was not able to fetch local storage")
            print_stack()
        return a

    def resetCook(self):
        """
        U JS stranice sam video da postoji globalna promenljiva 'cook' koja belezi rezultat.
        Posto se resetuje samo pri ucitavanju stranice, mislio sam da je efikasnije da je sam
        resetujem na 0 pri svakoj iteraciji umesto da reloadujem stranicu.
        Alternativa bi bila self.driver.refresh()
        """
        r = True
        try:
            self.driver.execute_script("window.cook = 0;")
            self.log.info("Variable cook was successfully reset")
        except:
            self.log.info("Cannot reset variable cook")
            r = False
            print_stack()
        return r

    def hover(self, locator="", locatorType='xpath', element=None):
        """
        Hovers pointer to an element.
        """
        r = True
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.perform()
            self.log.info("Successfully hovered to the element")
        except:
            self.log.error("Failed to hover to the element")
            print_stack()
            r = False
        return r
