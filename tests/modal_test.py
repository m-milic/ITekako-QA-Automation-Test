import time

from pages.modal_page import ModalPage
from utilities.teststatus import TestStatus
import unittest
import pytest

@pytest.mark.usefixtures("oneTimeSetUpLaterTests", "setUp")
class ModalTest(unittest.TestCase):

    sp = []

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUpLaterTests):
        self.sp = ModalPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order = 1)
    def test_allButtons(self):

        time.sleep(1)
        self.sp.driver.get(self.sp.driver.current_url + "/entry_ad")
        time.sleep(1)

        r = self.sp.isModalOpened(expected="Yes")
        self.ts.mark(r, "Checking if modal is opened on first page load")

        r = self.sp.closeModal()
        self.ts.mark(r, "Closing the modal and checking if it is closed")

        r = self.sp.reloadAndCheck()
        self.ts.mark(r, "Reloading and checking if modal is opened after")

        r = self.sp.deleteReloadAnCheck()
        self.ts.markFinal("Modal test", r, "Deleting cookie, reloading and checking if modal is opened")

        time.sleep(2)

