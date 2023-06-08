import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
import random
import time



class HoverPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators

    _first_image = "//h5[text()='name: user1']/../.."
    _first_name = "//h5[text()='name: user1']"
    _first_link = "//h5[text()='name: user1']/following-sibling::a"

    _second_image = "//h5[text()='name: user2']/../.."
    _second_name = "//h5[text()='name: user2']"
    _second_link = "//h5[text()='name: user2']/following-sibling::a"

    _third_image = "//h5[text()='name: user3']/../.."
    _third_name = "//h5[text()='name: user3']"
    _third_link = "//h5[text()='name: user3']/following-sibling::a"

    def hoverAndClickFirst(self, imgloc=_first_image, nmloc=_first_name, linkloc=_first_link, expurl="users/1", bk=0):
        if bk:
            self.driver.back()

        image = self.getElement(imgloc)
        name = self.getElement(nmloc)
        link = self.getElement(linkloc)
        r = bool(image) and bool(link)

        r = r & (not self.isElementDisplayed(element=name))

        r = r & self.hover(element=image)

        r = r & self.isElementDisplayed(element=name)

        r = r & self.hover(element=link)
        r = r & self.elementClick(element=link)

        url = self.driver.current_url[-7::]
        self.log.error("End of current url is: " + url)
        r = r & (url == expurl)
        return r

    def hoverAndClickSecond(self):
        r = self.hoverAndClickFirst(self._second_image, self._second_name, self._second_link, "users/2", 1)
        return r

    def hoverAndClickThird(self):
        r = self.hoverAndClickFirst(self._third_image, self._third_name, self._third_link, "users/3", 1)
        return r

