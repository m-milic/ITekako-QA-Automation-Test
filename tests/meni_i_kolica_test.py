import time
from pages.meni_i_kolica_page import MeniPage
from utilities.teststatus import TestStatus
import unittest
import pytest

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class MeniTest(unittest.TestCase):

    sp = []

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.sp = MeniPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order = 1)
    def test_menu_and_basket(self):
        """
        Test runs kind of slow, and has a lot of sleeps, because elements load slowly and Cart reactions are slow.
        Scrolls&sleeps at the beginning to load all the items, before creating internal Menu.
        Can be ran faster, by passing t = 0 to the addRandomtoBasket function, to remove wait between adding 2 itmes.
        This however always results in incorrect Total price in the Cart. At around 3s it becomes stable. 2s is default.
        """
        r = self.sp.openPage()
        self.ts.mark(r, "Opening page")
        time.sleep(1)

        self.sp.webScroll()
        time.sleep(1)

        r = self.sp.createMenu()
        self.ts.mark(r, "Initiating internal menu")

        r = self.sp.addRandomtoBasket(t=3)
        self.ts.mark(r, "Adding 6 random items to the basket")
        time.sleep(3)

        r = self.sp.returnItemList()
        self.ts.mark(r, "Fetching and logging list of items")           # Logs on Debug level

        r = self.sp.checkTotalPrice()
        self.ts.markFinal("Test Menu and Basket", r, "Checking Total Price")
        time.sleep(5)