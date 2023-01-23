import time

from pages.preporuka_page import PreporukaPage
from utilities.teststatus import TestStatus
import unittest
import pytest

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class PreporukaTest(unittest.TestCase):

    sp = []

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.sp = PreporukaPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order = 1)
    def test_allButtons(self):
        r = self.sp.openPage()
        self.ts.mark(r, "Opening page")
        time.sleep(1)

        self.sp.webScroll()                           # Could cause trouble on very small displays...Comment out if so.
        time.sleep(1)                                 # Could have been sorted out with more try/exc, but I'd need time.

        r = self.sp.clcikAndVerifyAll()
        self.ts.mark(r, "Verifying all left buttons/answers")
        time.sleep(1)

        r = self.sp.clearAll()
        self.ts.mark(r, "Clearing all fields")
        time.sleep(1)

        r = self.sp.clcikAndVerifyAll("negativni")
        self.ts.markFinal("All buttons test", r, "Verifying all right buttons/answers")
        time.sleep(1)

    @pytest.mark.run(order = 2)
    def test_allRecommendations(self):
        r = self.sp.verifyAllOptions()
        self.ts.markFinal("All Recommendations Test", r, "Verifying all recommendation options")
        time.sleep(2)