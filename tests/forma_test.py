import time

from pages.forma_page import FormaPage
from utilities.teststatus import TestStatus
import unittest
import pytest

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class FormaTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.sp = FormaPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order = 0)
    def test_1AllFields(self):
        r = self.sp.openPage()
        self.ts.mark(r, "Opening page")
        time.sleep(1)
        r = self.sp.selectIfAlergies()                # Selects if there are alergies. Accepts y, n or m. Default is y
        self.ts.mark(r, "Selecting if there are alergies")

        r = self.sp.enterOrganizer()                  # Takes string (name). Default name is set.
        self.ts.mark(r, "Entering Organizer")

        r = self.sp.enterCelebrant()                   # Takes string (name). Default name is set.
        self.ts.mark(r, "Entering Birthday Person")

        r = self.sp.enterAge()                        # Takes numeric string (age)
        self.ts.mark(r, "Entering Age")

        r = self.sp.enterDate()                       # Takes current date as default. Accepts ddmmyyyy format
        self.ts.mark(r, "Entering Date")

        r = self.sp.enterTime()                       # Takes current time as default. Accepts hhmm format
        self.ts.mark(r, "Entering Time")

        r = self.sp.selectPeople()                    # Takes option number 1-4. Option 2 selected by default
        self.ts.mark(r, "Selecting people")

        r = self.sp.checkAlergies()                   # Checks 1-n random alergies. 6 is default (and max), 1 is min
        self.ts.markFinal("Filling Fields Test", r, "Checking alergies")
        time.sleep(2)

    @pytest.mark.run(order = 1)
    def test_2Local_Storage(self):
        # self.sp.openPage()
        # time.sleep(2)                                         Uncomment these fields to run test individually
        # r = self.sp.enterAllFields()
        # self.ts.mark(r, "Was able to enter all fields?")
        r = self.sp.checkLocalStorage()                # Compares website LS to expected LS
        self.ts.markFinal("Local Storage Test", r, "Verifying local storage")

    @pytest.mark.run(order = 2)
    def test_3Confirmation_Window(self):
        # self.sp.openPage()
        # time.sleep(2)                                         Uncomment these fields to run test individually
        # r = self.sp.enterAllFields()
        # self.ts.mark(r, "Was able to enter all fields?")
        r = self.sp.clickFinish()
        self.ts.mark(r, "Was able to click Finish?")
        r = self.sp.checkConfirmation()                # Compares displayed Confirmation Window to expected values
        self.ts.markFinal("Confirmation Window Test", r, "Verifying confirmation window")
        time.sleep(2)
