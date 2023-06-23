import time

from pages.hover_page import HoverPage
from utilities.teststatus import TestStatus
import unittest
import pytest

@pytest.mark.usefixtures("oneTimeSetUpLaterTests", "setUp")
class HoverTest(unittest.TestCase):

    sp = []

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUpLaterTests):
        self.sp = HoverPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order = 1)
    def test_allButtons(self):

        time.sleep(1)
        self.sp.driver.get(self.sp.driver.current_url + "/hovers")

        r = self.sp.hoverAndClickFirst()
        self.ts.mark(r, "Hover and click first user")

        r = self.sp.hoverAndClickSecond()
        self.ts.mark(r, "Hover and click second user")

        r = self.sp.hoverAndClickThird()
        self.ts.markFinal("Hover and click test", r, "Hover and click first user")

        time.sleep(2)

