import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
import random
import time


class MenuItem:
    """
    This class is just to make it a bit easier for myself to work with store objects.
    It just takes price as a string, and button as a locator, and sets them as objects attributes.
    """

    def __init__(self, price, button):
        self.price = price
        self.button = button


class MeniPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators

    _link = "//a[@href = '/menu']"

    """
    Locators of prices and + button for menu options, and locator for list of items in the cart.
    Non specific - getting them will return a list.
    """
    _food_prices = "//h3[contains(text(), 'Food')]/../..//span"
    _food_buttons = "//h3[contains(text(), 'Food')]/../..//button"
    _desert_prices = "//h3[contains(text(), 'Desserts')]/../..//span"
    _desert_buttons = "//h3[contains(text(), 'Desserts')]/../..//button"
    _item_list = "//ul[@id='listaItema']/li"

    _total_displayed = "ukupno"  # ID     total price in cart

    # Storage
    """
    Food and desert names for use inside of the test. can be anything esle also
    """
    food_names = ["stuffed_veal", "chicken_parsley", "breaded_zucchini",
                  "skewered_pork", "mussels", "catfish", "mango_chicken", "beef_gozleme"]
    desert_names = ["Pancakes", "Strawberry", "Chocolate", "Malaga", "Baklava"]

    """ 
    Below, defining a dictionary, that will have food and desert names as keys,
    and objects of class MenuItems as values.
    """
    all_food = {}
    total_expected = 0

    def openPage(self):
        """
        Opens the Problem 3 page by clicking on a header link from the homepage
        """
        r = self.elementClick(self._link)
        return r

    def createMenu(self):
        """
        Core function, fills 'all_food' Dictionary with name : MenuItem(price, button), for all food and desert items.
        Makes it easier to get instant access to price/button via item name.
        """
        a = self.getElementList(self._food_buttons)
        b = self.getElementList(self._food_prices)
        r = bool(a) and bool(b)
        for i in range(len(a)):
            price = self.getText(element = b[i], info = self.food_names[i])[1:]
            self.all_food[self.food_names[i]] = MenuItem(price, a[i])
            r = r and bool(price)
        c = self.getElementList(self._desert_buttons)
        d = self.getElementList(self._desert_prices)
        r = r and bool(c) and bool(d)
        for i in range(len(c)):
            price = self.getText(element = d[i], info = self.desert_names[i])[1:]
            self.all_food[self.desert_names[i]] = MenuItem(price, c[i])
            r = r and bool(price)
        return r

    def addFToBasket(self, b):
        """
        Adds an item to the basket, and adds its price to expected Total of basket.
        ::b:: represents item's index (by index it's key has in the key's list).
        """
        item = self.all_food[b]
        a = int(item.price)
        self.total_expected += a
        r = bool(self.elementClick(element = item.button))
        return r

    def addRandomtoBasket(self, n = 6, t=2):
        """
        Logic of adding 'n' random items to the Cart - at least one of each kind, and at least one two times.
        n predefined as 6, and assigned 3 as the lowest option, to be able to meet the conditions.
        """
        if n < 3:
            n = 3
        r = True
        fc = 0                                                  # counter for Food items added to basket
        added = []                                              # list of keys(str) of added items
        for i in range(n):
            if random.randint(0, 1):
                a = random.randint(0, 7)
                current = self.food_names[a]
                fc = 1
            else:
                a = random.randint(0, 4)
                current = self.desert_names[a]
            time.sleep(t)
            r = r and bool(self.addFToBasket(current))
            added.append(current)
            if i == n-3 and fc == 0:                            # when 2 items are yet to be added, ads food if none
                x = self.food_names[random.randint(0, 7)]       # and increases iterator by one
                r = r and bool(self.addFToBasket(x))
                added.append(x)
                i += 1
            if i == n-2 and (len(added) == len(set(added))):    # 1 item before end, adds last one if there are no
                time.sleep(t)                                   # duplicates, and breaks the loop. Checks this by
                r = r and bool(self.addFToBasket(current))      # comparing length of set and list of added items
                added.append(current)
                break
        return r

    def returnItemList(self):
        """
        Fetches and returns the list of strings of all entries in the Cart on the page.
        Not needed for the Problem, but useful for debugging the test.
        """
        a = self.getElementList(self._item_list)
        b = []
        j = 0
        for i in range(len(a)):
            b.append(self.getText(element = a[i], info = ("Basket item " + str(i+1))))
            j += 1
        self.log.debug(b)
        return b

    def getTotalPrice(self):
        """
        Fetches and returns Total price displayed in the Cart.
        """
        a = int(self.getText(self._total_displayed, locatorType="ID", info="Total Price"))
        return a

    def checkTotalPrice(self):
        """
        Compares Total price displayed in the Cart to the total expected price.
        """
        a = self.getTotalPrice()
        b = self.total_expected
        r = bool(a)
        if a == b:
            self.log.info("Total price is as expected.")
        else:
            self.log.info("Total price is not as expected. Expected: " + str(b) + " ; Displayed: " + str(a))
            r = False
        return r
