import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
import random
import time



class ModalPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators

    _modal_whole = "modal"  # ID  - has attribute style="display: .." reffering to if it's displayed
    _modal_close = "//div[@class='modal-footer']/p"

    _third_link = "//h5[text()='name: user3']/following-sibling::a"

    # Functions

    def isModalOpened(self, expected="Yes"):
        style = self.getAttribute("style", locator=self._modal_whole, locatorType="ID")
        if expected=="Yes":
            r = (style=="display: block;")
        else:
            r = (style=="display: none;")
        return r

    def closeModal(self):
        r = self.elementClick(self._modal_close)
        time.sleep(1)
        r = r & self.isModalOpened(expected = "No")
        return r

    def deleteCoookie(self):
        self.driver.delete_cookie("rack.session")
        r = (not bool(self.driver.get_cookie("rack.session")))
        return r

    def reloadAndCheck(self):
        self.driver.refresh()
        time.sleep(1)
        r = self.isModalOpened(expected="No")
        return r

    def deleteReloadAnCheck(self):
        r = self.deleteCoookie()
        self.driver.refresh()
        time.sleep(1)
        r = r & self.isModalOpened(expected="Yes")
        return r

